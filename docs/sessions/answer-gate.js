/**
 * 解答例の公開日制御
 *
 * 使い方:
 *   <section id="answers-section" data-release="2026-04-22">
 *     <div id="answers-locked" style="display:none">...</div>
 *     <div id="answers-content">...解答...</div>
 *   </section>
 *   <script src="answer-gate.js"></script>
 *
 * data-release の日付（JST 0:00）より前 → 解答を非表示、ロックメッセージ表示
 * data-release の日付以降 → 解答を表示
 */
(function() {
  var section = document.getElementById('answers-section');
  if (!section) return;

  var release = section.getAttribute('data-release');
  if (!release) return;

  var releaseDate = new Date(release + 'T00:00:00+09:00');
  var now = new Date();

  if (now < releaseDate) {
    var content = document.getElementById('answers-content');
    var locked = document.getElementById('answers-locked');
    if (content) content.style.display = 'none';
    if (locked) {
      locked.style.display = 'block';
      var display = document.getElementById('release-date-display');
      if (display) {
        display.textContent = (releaseDate.getMonth() + 1) + '月' + releaseDate.getDate() + '日';
      }
    }
  }
})();
