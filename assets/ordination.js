// หน้าโครงการบวชบูชาธรรม 84 ปี — โหลดกำหนดการ/ข้อความล่าสุดจากระบบผู้ดูแล และส่งใบสมัครเข้าทะเบียนกลาง
(function () {
  'use strict';
  var body = document.body;
  var LANG = body.getAttribute('data-lang') === 'ja' ? 'ja' : 'th';
  var API = (new URLSearchParams(location.search).get('api') || body.getAttribute('data-api')).replace(/\/$/, '');

  var I18N = {
    th: {
      roundWord: function (n) { return 'รอบที่ ' + n; }, roundNo: function (n) { return '<span class="text-xs">รอบที่</span>' + n; },
      training: 'ช่วงอบรม', ceremony: 'วันอุปสมบท / วันงาน', apply: 'สมัครรอบนี้ →',
      st: { open: 'เปิดรับสมัคร', upcoming: 'เร็ว ๆ นี้', closed: 'ปิดรับสมัคร', done: 'เสร็จสิ้นแล้ว' },
      closeOn: function (d) { return 'รับสมัครถึง ' + fmtDate(d); },
      otherTemple: 'วัดอื่น / ยังไม่มีวัดต้นสังกัด',
      required: 'กรุณากรอกช่องนี้', chooseRound: 'กรุณาเลือกรอบ', roundClosed: 'รอบนี้ปิดรับสมัครแล้ว กรุณาเลือกรอบอื่น',
      chooseTemple: 'กรุณาเลือกวัดต้นสังกัด หรือระบุชื่อวัด', consent: 'กรุณายืนยันการให้ใช้ข้อมูล', email: 'รูปแบบอีเมลไม่ถูกต้อง',
      fixErrors: 'ยังกรอกข้อมูลไม่ครบ กรุณาตรวจสอบช่องที่มีข้อความสีแดง',
      sending: 'กำลังส่งใบสมัคร…', submit: 'ส่งใบสมัคร',
      tooMany: 'มีการส่งใบสมัครจากเครือข่ายนี้หลายครั้งเกินไป กรุณารอสักครู่แล้วลองใหม่ หรือติดต่อ LINE ID: ppkaw075',
      netErr: 'ส่งใบสมัครไม่สำเร็จ กรุณาตรวจสอบอินเทอร์เน็ตแล้วลองใหม่ หากยังไม่ได้ กรุณาติดต่อ LINE ID: ppkaw075',
      loadErr: 'ขณะนี้โหลดข้อมูลรอบบวชไม่ได้ กรุณารีเฟรชหน้านี้อีกครั้ง หรือสมัครผ่าน LINE ID: ppkaw075',
      noOpen: 'ขณะนี้ยังไม่มีรอบที่เปิดรับสมัคร กรุณาติดตามประกาศ หรือติดต่อ LINE ID: ppkaw075',
      doneTitle: 'ได้รับใบสมัครแล้ว ขออนุโมทนาบุญ',
      doneBody: function (name, round) { return 'คุณ' + name + ' สมัคร' + round + ' เรียบร้อยแล้ว ทีมงานจะติดต่อกลับทางโทรศัพท์หรือ LINE เพื่อนัดสัมภาษณ์และตรวจเอกสาร'; },
      doneRef: 'รหัสใบสมัครของท่าน (โปรดจดไว้)', doneAgain: 'สมัครให้อีกท่านหนึ่ง', copied: '✓ คัดลอกแล้ว',
    },
    ja: {
      roundWord: function (n) { return '第' + n + '回'; }, roundNo: function (n) { return '<span class="text-xs">第</span>' + n + '<span class="text-xs">回</span>'; },
      training: '研修期間', ceremony: '得度式の日', apply: 'この回に申し込む →',
      st: { open: '受付中', upcoming: '近日受付', closed: '受付終了', done: '終了' },
      closeOn: function (d) { return d.replace(/^(\d{4})-(\d{2})-(\d{2})$/, function (_, y, m, dd) { return y + '年' + Number(m) + '月' + Number(dd) + '日'; }) + 'まで受付'; },
      otherTemple: 'その他の寺院・所属なし',
      required: '入力してください', chooseRound: '参加する回を選んでください', roundClosed: 'この回の受付は終了しました。別の回を選んでください',
      chooseTemple: '所属寺院を選ぶか、寺院名をご記入ください', consent: '個人情報の利用に同意してください', email: 'メールアドレスの形式が正しくありません',
      fixErrors: '未入力の項目があります。赤字の箇所をご確認ください',
      sending: '送信しています…', submit: '申込を送信する',
      tooMany: '短時間に送信が集中しています。しばらく待ってから再度お試しいただくか、LINE ID: ppkaw075 までご連絡ください',
      netErr: '送信できませんでした。通信環境をご確認のうえ再度お試しください。解決しない場合は LINE ID: ppkaw075 までご連絡ください',
      loadErr: '日程を読み込めませんでした。ページを再読み込みするか、LINE ID: ppkaw075 までご連絡ください',
      noOpen: '現在受付中の回はありません。お知らせをお待ちいただくか、LINE ID: ppkaw075 までお問い合わせください',
      doneTitle: 'お申し込みを受け付けました',
      doneBody: function (name, round) { return name + ' 様の' + round + 'へのお申し込みを受け付けました。面談と書類確認のため、担当者から電話またはLINEでご連絡いたします。'; },
      doneRef: '受付番号（お控えください）', doneAgain: '別の方を申し込む', copied: '✓ コピーしました',
    },
  }[LANG];

  var state = { rounds: [], temples: [], loaded: false };
  var form = document.getElementById('reg-form');

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function lines(s) { return String(s || '').split('\n').map(function (x) { return x.trim(); }).filter(Boolean); }
  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || '');
    if (!m) return d;
    var th = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
    return Number(m[3]) + ' ' + th[Number(m[2]) - 1] + ' ' + (Number(m[1]) + 543);
  }

  // ---------- ข้อความจากหน้าผู้ดูแล ----------
  function applyContent(content) {
    document.querySelectorAll('[data-c]').forEach(function (el) {
      var key = el.getAttribute('data-c');
      var item = content[key];
      if (!item) return;
      var text = item[LANG] || '';
      var kind = el.getAttribute('data-kind');
      if (kind === 'list') {
        el.innerHTML = lines(text).map(function (x) { return '<li class="flex gap-2"><span class="text-accent mt-0.5">◆</span><span>' + esc(x) + '</span></li>'; }).join('');
      } else if (kind === 'pairs') {
        el.innerHTML = lines(text).map(function (x) {
          var p = x.split('|');
          return '<li><span class="text-primary">' + esc(p[0].trim()) + '</span> <strong class="text-dark">' + esc((p.slice(1).join('|')).trim()) + '</strong></li>';
        }).join('');
      } else if (kind === 'process') {
        el.innerHTML = lines(text).map(function (x, i) {
          var p = x.split('|');
          return '<div class="proc-card"><div class="proc-no">' + (i + 1) + '</div><h3 class="font-serif font-bold text-xl text-dark mb-2">' + esc(p[0].trim()) +
            '</h3><p class="text-dark/70 leading-relaxed">' + esc(p.slice(1).join('|').trim()) + '</p></div>';
        }).join('');
      } else if (text || key === 'announcement') {
        el.textContent = text;
      }
    });
    var ann = content.announcement && content.announcement[LANG];
    document.getElementById('announcement').classList.toggle('hidden', !ann);
  }

  // ---------- กำหนดการ ----------
  function roundLabel(r) { return r['label_' + LANG]; }
  function renderRounds() {
    var box = document.getElementById('rounds');
    box.innerHTML = state.rounds.map(function (r) {
      var note = r['note_' + LANG];
      var closeLine = r.status === 'open' && r.reg_close ? '<div class="text-xs text-primary">' + esc(I18N.closeOn(r.reg_close)) + '</div>' : '';
      return '<div class="round-card">' +
        '<div class="round-no">' + I18N.roundNo(esc(r.no)) + '</div>' +
        '<div class="flex-1 min-w-0"><div class="font-serif font-bold text-lg text-dark">' + esc(roundLabel(r)) + '</div>' +
        '<div class="grid sm:grid-cols-2 gap-x-6 gap-y-1 mt-2 text-sm">' +
        '<div><span class="text-primary">' + I18N.training + '</span><div class="font-semibold text-dark">' + esc(r['training_' + LANG]) + '</div></div>' +
        '<div><span class="text-primary">' + I18N.ceremony + '</span><div class="font-semibold text-dark">' + esc(r['ceremony_' + LANG]) + '</div></div></div>' +
        (note ? '<div class="round-note">' + esc(note) + '</div>' : '') + '</div>' +
        '<div class="round-side"><div class="text-right"><span class="badge badge-' + r.status + '">' + esc(I18N.st[r.status] || r.status) + '</span>' + closeLine + '</div>' +
        (r.status === 'open' ? '<a href="#register" data-round="' + r.id + '" class="round-apply">' + I18N.apply + '</a>' : '') + '</div></div>';
    }).join('');
    var stat = document.getElementById('stat-rounds');
    if (stat) stat.textContent = state.rounds.length;
  }

  function renderRoundOptions() {
    var box = document.getElementById('round-options');
    var open = state.rounds.filter(function (r) { return r.status === 'open'; });
    if (!open.length) {
      box.innerHTML = '<div class="form-alert info sm:col-span-2">' + esc(I18N.noOpen) + '</div>';
      document.getElementById('reg-submit').disabled = true;
      return;
    }
    box.innerHTML = state.rounds.filter(function (r) { return r.status !== 'done'; }).map(function (r) {
      var dis = r.status !== 'open';
      return '<label class="choice"><input type="radio" name="round_id" value="' + r.id + '"' + (dis ? ' disabled' : '') + '>' +
        '<span><b>' + esc(I18N.roundWord(r.no)) + ' · ' + esc(roundLabel(r)) + '</b><small>' + esc(I18N.ceremony) + ': ' + esc(r['ceremony_' + LANG]) +
        (dis ? ' · ' + esc(I18N.st[r.status]) : '') + '</small></span></label>';
    }).join('');
  }

  function renderTemples() {
    var sel = document.getElementById('f-temple');
    var first = sel.options[0].outerHTML;
    sel.innerHTML = first + state.temples.map(function (t) {
      var name = t['name_' + LANG] || t.name_th;
      var note = t['note_' + LANG];
      return '<option value="' + t.id + '">' + esc(name + (note ? ' (' + note + ')' : '')) + '</option>';
    }).join('') + '<option value="other">' + esc(I18N.otherTemple) + '</option>';
  }

  function load() {
    fetch(API + '/api/public/config', { mode: 'cors' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        state.rounds = d.rounds || [];
        state.temples = d.temples || [];
        state.loaded = true;
        applyContent(d.content || {});
        renderRounds();
        renderRoundOptions();
        renderTemples();
        preselectFromHash();
      })
      .catch(function () {
        showAlert(I18N.loadErr);
        document.getElementById('reg-submit').disabled = true;
      });
  }

  // ---------- ฟอร์ม ----------
  function selectRound(id) {
    var input = form.querySelector('input[name="round_id"][value="' + id + '"]');
    if (input && !input.disabled) { input.checked = true; clearErr('round_id'); }
  }
  function preselectFromHash() {
    var m = /round=(\d+)/.exec(location.hash);
    if (m) selectRound(m[1]);
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('[data-round]');
    if (a && state.loaded) selectRound(a.getAttribute('data-round'));
  });

  document.getElementById('f-temple').addEventListener('change', function () {
    var other = document.getElementById('f-temple-other');
    var isOther = this.value === 'other';
    other.classList.toggle('hidden', !isOther);
    if (isOther) other.focus();
  });
  form.addEventListener('change', function (ev) {
    if (ev.target.name === 'ordained_before') document.getElementById('before-detail').classList.toggle('hidden', ev.target.value !== 'yes');
    if (ev.target.name) clearErr(ev.target.name === 'temple_other' ? 'temple_id' : ev.target.name);
  });
  form.addEventListener('input', function (ev) { if (ev.target.name) clearErr(ev.target.name === 'temple_other' ? 'temple_id' : ev.target.name); });

  function group(name) { return form.querySelector('[data-field="' + name + '"]'); }
  function setErr(name, msg) {
    var g = group(name);
    if (!g) return;
    g.classList.add('has-err');
    g.querySelector('.ferr').textContent = msg;
  }
  function clearErr(name) {
    var g = group(name);
    if (g) g.classList.remove('has-err');
  }
  function showAlert(msg, info) {
    var a = document.getElementById('form-alert');
    a.textContent = msg;
    a.classList.toggle('info', !!info);
    a.classList.remove('hidden');
  }
  function hideAlert() { document.getElementById('form-alert').classList.add('hidden'); }

  function collect() {
    var fd = new FormData(form);
    var data = { lang: LANG };
    fd.forEach(function (v, k) { data[k] = typeof v === 'string' ? v.trim() : v; });
    data.consent = !!fd.get('consent');
    return data;
  }

  function validate(d) {
    var errs = {};
    if (!d.round_id) errs.round_id = I18N.chooseRound;
    if (!d.temple_id || (d.temple_id === 'other' && !d.temple_other)) errs.temple_id = I18N.chooseTemple;
    if (!d.full_name) errs.full_name = I18N.required;
    if (!d.birth_date) errs.birth_date = I18N.required;
    if (!d.phone) errs.phone = I18N.required;
    if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) errs.email = I18N.email;
    if (!d.consent) errs.consent = I18N.consent;
    return errs;
  }

  function showErrors(errs) {
    Object.keys(errs).forEach(function (k) { setErr(k, errs[k]); });
    showAlert(I18N.fixErrors);
    var first = form.querySelector('.has-err');
    if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    hideAlert();
    var d = collect();
    var errs = validate(d);
    if (Object.keys(errs).length) return showErrors(errs);
    var btn = document.getElementById('reg-submit');
    btn.disabled = true;
    btn.textContent = I18N.sending;
    fetch(API + '/api/public/register', { method: 'POST', mode: 'cors', headers: { 'content-type': 'application/json' }, body: JSON.stringify(d) })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (res) {
        if (res.status === 200 && res.body.ok) return done(d, res.body.ref);
        if (res.status === 422 && res.body.fields) {
          var map = {};
          Object.keys(res.body.fields).forEach(function (k) {
            var code = res.body.fields[k];
            map[k] = code === 'round_closed' ? I18N.roundClosed : k === 'email' ? I18N.email : k === 'consent' ? I18N.consent :
              k === 'round_id' ? I18N.chooseRound : k === 'temple_id' ? I18N.chooseTemple : I18N.required;
          });
          return showErrors(map);
        }
        showAlert(res.status === 429 ? I18N.tooMany : I18N.netErr);
      })
      .catch(function () { showAlert(I18N.netErr); })
      .then(function () { btn.disabled = false; btn.textContent = I18N.submit; });
  });

  function done(d, ref) {
    var round = state.rounds.filter(function (r) { return String(r.id) === String(d.round_id); })[0];
    var box = document.getElementById('reg-done');
    box.innerHTML = '<div class="done-ic">✓</div>' +
      '<h3 class="font-serif text-2xl font-bold text-dark mb-3">' + esc(I18N.doneTitle) + '</h3>' +
      '<p class="text-dark/75 max-w-lg mx-auto leading-relaxed">' + esc(I18N.doneBody(d.full_name, round ? I18N.roundWord(round.no) + ' (' + roundLabel(round) + ')' : '')) + '</p>' +
      '<p class="text-sm text-primary mt-6">' + esc(I18N.doneRef) + '</p><div class="done-ref">' + esc(ref) + '</div>' +
      '<div><button type="button" id="reg-again" class="btn-accent px-8 py-3">' + esc(I18N.doneAgain) + '</button></div>';
    form.classList.add('hidden');
    box.classList.remove('hidden');
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
    box.focus({ preventScroll: true });
    document.getElementById('reg-again').addEventListener('click', function () {
      form.reset();
      form.querySelectorAll('.has-err').forEach(function (g) { g.classList.remove('has-err'); });
      document.getElementById('f-temple-other').classList.add('hidden');
      document.getElementById('before-detail').classList.add('hidden');
      box.classList.add('hidden');
      form.classList.remove('hidden');
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // ---------- คัดลอกเลขบัญชี / ภาพ ----------
  document.querySelectorAll('.copy-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var orig = b.textContent;
      navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
        b.textContent = b.getAttribute('data-done');
        setTimeout(function () { b.textContent = orig; }, 2000);
      });
    });
  });
  var lb = document.getElementById('lightbox');
  document.querySelectorAll('.gal-item').forEach(function (g) {
    g.addEventListener('click', function () { lb.querySelector('img').src = g.getAttribute('data-full'); lb.classList.remove('hidden'); });
  });
  lb.addEventListener('click', function (ev) { if (ev.target.tagName !== 'IMG') lb.classList.add('hidden'); });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') lb.classList.add('hidden'); });

  load();
})();
