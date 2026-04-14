/**
 * 解答例の公開日時制御
 *
 * 使い方:
 *   <section id="answers-section" data-release="2026-04-22T14:40">
 *     <p id="answers-locked" style="display:none">...</p>
 *     <div id="answers-content">...解答...</div>
 *   </section>
 *   <script src="answer-gate.js"></script>
 *
 * data-release の日時（JST）より前 → 解答を非表示、ロックメッセージ表示
 * data-release の日時以降 → 解答を表示
 */
(function() {
  var section = document.getElementById('answers-section');
  if (!section) return;

  var release = section.getAttribute('data-release');
  if (!release) return;

  // "2026-04-22T14:40" → JST として解釈
  var releaseDate;
  if (release.indexOf('T') !== -1) {
    releaseDate = new Date(release + ':00+09:00');
  } else {
    releaseDate = new Date(release + 'T00:00:00+09:00');
  }

  var now = new Date();

  if (now < releaseDate) {
    var content = document.getElementById('answers-content');
    var locked = document.getElementById('answers-locked');
    if (content) content.style.display = 'none';
    if (locked) {
      locked.style.display = 'block';
      var display = document.getElementById('release-date-display');
      if (display) {
        var m = releaseDate.getMonth() + 1;
        var d = releaseDate.getDate();
        var h = releaseDate.getHours();
        var min = ('0' + releaseDate.getMinutes()).slice(-2);
        display.textContent = m + '月' + d + '日 ' + h + ':' + min;
      }
    }
  }
})();
