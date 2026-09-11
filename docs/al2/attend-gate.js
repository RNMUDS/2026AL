/**
 * 出席用の認証コードを、その回の授業時間だけ表示する。
 *
 * - 授業日の表示時間帯（data-window、JST）だけ、その回のコードを復号して表示する
 * - それ以外の時間は「次はいつ表示されるか」だけを出す
 * - スタッフ用パスワードを入れると、全回のコードを一覧で表示する
 *
 * 暗号形式は answer-gate.js と同じ（base64: salt16 + iv12 + tag16 + 暗号文、PBKDF2 100,000回）。
 * 静的ページなので、しくみ上「絶対に見られない」保証はない。
 * 実際の出席の締め切りは manaba / respon 側の受付時間で管理する。
 */
(function () {
  var box = document.getElementById('attend-box');
  if (!box) return;
  var cipherB64 = box.getAttribute('data-cipher');
  var windowText = box.getAttribute('data-window') || '14:30-16:30';
  var parts = windowText.split('-');
  var openAt = parts[0].split(':').map(Number);
  var closeAt = parts[1].split(':').map(Number);

  function jstNow() {
    var now = new Date();
    var utc = now.getTime() + now.getTimezoneOffset() * 60000;
    return new Date(utc + 9 * 3600000);
  }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function dateKey(d) { return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()); }
  function minutes(d) { return d.getHours() * 60 + d.getMinutes(); }

  function decrypt(b64, password) {
    var raw = Uint8Array.from(atob(b64), function (c) { return c.charCodeAt(0); });
    var salt = raw.slice(0, 16), iv = raw.slice(16, 28), tag = raw.slice(28, 44), body = raw.slice(44);
    var combined = new Uint8Array(body.length + tag.length);
    combined.set(body); combined.set(tag, body.length);
    return crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey'])
      .then(function (k) {
        return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
          k, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (aes) { return crypto.subtle.decrypt({ name: 'AES-GCM', iv: iv }, aes, combined); })
      .then(function (buf) { return JSON.parse(new TextDecoder().decode(buf)); })
      .catch(function () { return null; });
  }

  var _k = [97, 116, 116, 101, 110, 100, 45, 97, 108, 50, 45, 50, 48, 50, 54];
  var _p = _k.map(function (c) { return String.fromCharCode(c); }).join('');

  function render(sessions) {
    var now = jstNow();
    var today = dateKey(now);
    var m = minutes(now);
    var openM = openAt[0] * 60 + openAt[1], closeM = closeAt[0] * 60 + closeAt[1];
    var todays = null, next = null;
    for (var i = 0; i < sessions.length; i++) {
      var s = sessions[i];
      if (s.date === today) todays = s;
      if (s.date > today && !next) next = s;
    }
    if (todays && m >= openM && m <= closeM) {
      box.innerHTML =
        '<div class="attend-live">' +
          '<div class="attend-label">第' + todays.n + '回の出席コード</div>' +
          '<div class="attend-code">' + todays.code + '</div>' +
          '<div class="attend-note">respon に入力してください。表示は ' + windowText.replace('-', '〜') + ' の間だけです</div>' +
        '</div>';
      return;
    }
    var msg;
    if (todays && m < openM) {
      msg = '本日 第' + todays.n + '回の出席コードは <strong>' + windowText.split('-')[0] + '</strong> にここに表示されます';
    } else if (next) {
      var d = next.date.split('-');
      msg = '出席コードは授業の時間（水曜 ' + windowText.replace('-', '〜') + '）にここに表示されます。次回は <strong>' +
            parseInt(d[1], 10) + '月' + parseInt(d[2], 10) + '日（第' + next.n + '回）</strong>';
    } else {
      msg = '後期の授業はすべて終了しました';
    }
    box.innerHTML = '<div class="attend-wait">' + msg + '</div>' + staffForm();
    bindStaff(sessions);
  }

  function staffForm() {
    return '<details class="attend-staff"><summary>スタッフ用</summary>' +
      '<div style="display:flex;gap:0.5rem;align-items:center;margin-top:0.5rem">' +
      '<input type="password" id="attend-pass" placeholder="パスワード" ' +
      'style="background:#0A0A0A;color:#E0E0E0;border:1px solid #444;border-radius:6px;padding:0.4rem 0.8rem;font-size:0.85rem;width:160px">' +
      '<button id="attend-pass-btn" style="background:#4A7A00;color:white;border:none;border-radius:6px;padding:0.4rem 1rem;font-size:0.85rem;cursor:pointer;font-weight:600">全回を表示</button>' +
      '</div><p id="attend-pass-error" style="color:#FF5252;font-size:0.8rem;margin-top:0.4rem;display:none">パスワードが違います</p></details>';
  }

  function bindStaff(sessions) {
    var btn = document.getElementById('attend-pass-btn');
    var input = document.getElementById('attend-pass');
    if (!btn) return;
    function attempt() {
      decrypt(cipherB64, input.value).then(function (data) {
        if (!data) { document.getElementById('attend-pass-error').style.display = 'block'; return; }
        var rows = data.map(function (s) {
          var d = s.date.split('-');
          return '<tr><td>第' + s.n + '回</td><td>' + parseInt(d[1], 10) + '/' + parseInt(d[2], 10) + '</td><td class="attend-code-small">' + s.code + '</td></tr>';
        }).join('');
        box.innerHTML = '<table><tr><th>回</th><th>日付</th><th>コード</th></tr>' + rows + '</table>';
      });
    }
    btn.addEventListener('click', attempt);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') attempt(); });
  }

  decrypt(cipherB64, _p).then(function (data) {
    if (data) render(data);
    else box.innerHTML = '<div class="attend-wait">出席コードを読み込めませんでした</div>';
  });
})();
