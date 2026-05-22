<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Andromeda Bingo</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
:root {
  --orange:#f07020; --orange2:#fb923c;
  --indigo:#2d2b6b; --indigo-soft:#4a4899;
  --muted:#9b95c4; --bg:#c9b8e8;
  --green:#16a34a; --green2:#22c55e;
  --red:#e53935; --blue:#1e88e5;
  --purple:#8e24aa; --amber:#fb8c00;
  --dark:#2d1a4a; --white:#ffffff;
  --shadow:0 4px 24px rgba(80,60,140,.13),0 1.5px 6px rgba(80,60,140,.07);
}
html,body { height:100%; width:100%; overflow:hidden; font-family:'Outfit',sans-serif; background:#b5a3d8; -webkit-tap-highlight-color:transparent; }

/* ══ SCREEN SYSTEM ══ */
.screen { position:fixed; inset:0; display:flex; justify-content:center; transition:opacity .3s ease, transform .3s ease; }
.screen.hidden     { opacity:0; pointer-events:none; transform:translateX(48px); }
.screen.slide-away { opacity:0; pointer-events:none; transform:translateX(-48px); }

/* ══════════════════════════════════
   SCREEN 1 — LOBBY
══════════════════════════════════ */
#screen-lobby { background:#b5a3d8; overflow-y:auto; overflow-x:hidden; }
.shell {
  width:100%; max-width:420px; min-height:100%;
  background:var(--bg);
  background-image:radial-gradient(ellipse at 20% 0%,rgba(255,255,255,.22) 0%,transparent 60%),
    radial-gradient(ellipse at 80% 100%,rgba(160,130,220,.3) 0%,transparent 60%);
  padding:22px 15px 44px;
}
.top-row { display:grid; grid-template-columns:1fr 1fr; gap:11px; margin-bottom:18px; animation:fadeUp .4s .05s both; }
.top-card { background:#fff; border-radius:18px; padding:14px 15px; box-shadow:var(--shadow),inset 0 1px 0 rgba(255,255,255,.8); display:flex; align-items:center; gap:11px; cursor:pointer; transition:transform .15s; }
.top-card:active { transform:scale(.97); }
.ic { width:40px; height:40px; border-radius:12px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.ic svg { width:21px; height:21px; }
.ic-w { background:linear-gradient(135deg,#ffe8d0,#ffd0a0); }
.ic-r { background:linear-gradient(135deg,#e0deff,#cfc9ff); }
.tlbl { font-size:10.5px; font-weight:600; color:var(--muted); letter-spacing:.05em; text-transform:uppercase; }
.tval { font-size:17px; font-weight:800; color:var(--indigo); letter-spacing:-.02em; line-height:1.2; }
.tval.sm { font-size:14px; font-weight:700; }
.lobby-box { background:#fff; border-radius:24px; overflow:visible; box-shadow:0 8px 40px rgba(80,60,140,.18),0 2px 8px rgba(80,60,140,.08); animation:fadeUp .4s .15s both; }
.lhdr {
  background:linear-gradient(90deg,#e85d10,#f07020 50%,#f58c30);
  border-radius:22px 22px 0 0; padding:14px 14px;
  display:grid; grid-template-columns:1fr .85fr .85fr 1.2fr .85fr;
  align-items:center; position:relative; overflow:hidden;
}
.lhdr::after { content:''; position:absolute; top:-40%; right:-10%; width:170px; height:170px; background:radial-gradient(circle,rgba(255,255,255,.1) 0%,transparent 70%); border-radius:50%; pointer-events:none; }
.hcol { font-size:11.5px; font-weight:800; color:#fff; text-align:center; letter-spacing:.02em; text-shadow:0 1px 3px rgba(0,0,0,.15); }
.hcol:first-child { text-align:left; } .hcol:last-child { text-align:right; }
.l-rows { padding:14px 10px 16px; display:flex; flex-direction:column; gap:16px; }
.row-outer { position:relative; margin-top:6px; }
.badge { position:absolute; top:-13px; left:50%; transform:translateX(-50%); background:#fff; border:1.5px solid var(--orange); border-radius:30px; padding:3px 12px; font-size:11px; font-weight:800; color:var(--orange); white-space:nowrap; z-index:10; display:flex; align-items:center; gap:5px; box-shadow:0 2px 10px rgba(240,112,32,.18); }
.bdot { width:7px; height:7px; border-radius:50%; background:var(--orange); animation:pdot 1.4s ease-in-out infinite; }
@keyframes pdot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.65)} }
.grow { background:#fff; border-radius:16px; padding:14px 13px; display:grid; grid-template-columns:1fr .85fr .85fr 1.2fr .85fr; align-items:center; box-shadow:0 2px 14px rgba(80,60,140,.08); border:1.5px solid rgba(200,190,230,.35); transition:opacity .4s,border-color .4s; }
.grow.dim { opacity:.82; border-color:rgba(240,112,32,.2); }
.lstake { font-size:14px; font-weight:800; color:var(--indigo); }
.lscell { text-align:center; } .lpcell { text-align:center; font-size:13.5px; font-weight:700; color:var(--indigo-soft); }
.ldcell { text-align:center; font-size:12px; font-weight:700; color:var(--indigo); }
.ldcell small { display:block; font-size:9px; font-weight:600; color:var(--muted); letter-spacing:.03em; margin-top:1px; }
.lplaycell { display:flex; justify-content:flex-end; }
.b-timer { font-size:13px; font-weight:800; color:var(--orange); background:rgba(240,112,32,.12); border-radius:8px; padding:3px 8px; display:inline-block; min-width:34px; text-align:center; }
.b-timer.urg { color:#d93020; background:rgba(217,48,32,.13); animation:blink .5s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.5} }
.btn-play { background:linear-gradient(160deg,#ff9040,#f06018); color:#fff; border:none; border-radius:12px; padding:9px 15px; font-family:'Outfit',sans-serif; font-size:13px; font-weight:800; cursor:pointer; box-shadow:0 4px 14px rgba(240,112,32,.38); transition:transform .12s; }
.btn-play:active { transform:scale(.91); }
.btn-disabled { background:rgba(180,170,210,.18); color:var(--muted); border:1.5px solid rgba(155,149,196,.22); border-radius:12px; padding:9px 11px; font-family:'Outfit',sans-serif; font-size:12px; font-weight:700; cursor:default; }
@keyframes fadeUp { from{opacity:0;transform:translateY(13px)} to{opacity:1;transform:translateY(0)} }

/* ══════════════════════════════════
   SCREEN 2 — CARTELA PICKER
══════════════════════════════════ */
#screen-cartela { background:var(--bg); overflow:hidden; }
.picker-shell { width:100%; max-width:430px; height:100dvh; display:flex; flex-direction:column; overflow:hidden; }
.picker-header { flex-shrink:0; padding:8px 10px 5px; display:grid; grid-template-columns:auto 1fr 1fr 1fr; gap:6px; align-items:stretch; }
.back-btn { background:var(--white); border:none; border-radius:14px; width:42px; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 10px rgba(0,0,0,.10); transition:transform .12s; }
.back-btn:active { transform:scale(.9); }
.hcard { background:var(--white); border-radius:14px; padding:8px 6px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,.10); gap:2px; }
.hcard .lbl { font-size:7px; font-weight:800; color:var(--muted); text-transform:uppercase; letter-spacing:.10em; line-height:1; }
.hcard .val { font-size:13px; font-weight:900; color:var(--dark); line-height:1; font-family:'Nunito',sans-serif; }
.wallet-val { color:#059669 !important; }
.stake-val  { color:#7c3aed !important; }
.cd-card .val { color:var(--orange) !important; font-size:15px !important; }
.cd-card .val.urg { color:#d93020 !important; animation:blink .5s ease-in-out infinite; }
.pool-scroll { flex:1; min-height:0; overflow-y:auto; overflow-x:hidden; -webkit-overflow-scrolling:touch; padding:3px 8px 4px; scrollbar-width:none; }
.pool-scroll::-webkit-scrollbar { display:none; }
.pool-grid { display:grid; grid-template-columns:repeat(10,1fr); gap:2px; }
.pool-cell { aspect-ratio:1; border-radius:7px; background:var(--white); display:flex; align-items:center; justify-content:center; font-family:'Nunito',sans-serif; font-size:clamp(6px,1.8vw,10px); font-weight:800; color:#5b4e7a; user-select:none; cursor:pointer; box-shadow:0 1px 3px rgba(0,0,0,.07); transition:background .18s,color .18s,transform .12s; }
.pool-cell:active { transform:scale(.88); }
.pool-cell.active { background:linear-gradient(135deg,var(--green),var(--green2)); color:#fff; transform:scale(1.12); z-index:2; box-shadow:0 0 0 2px rgba(34,197,94,.45),0 0 12px rgba(22,163,74,.5); animation:cell-pop .38s cubic-bezier(.36,.07,.19,.97) both; }
@keyframes cell-pop { 0%{transform:scale(.65);opacity:.3} 55%{transform:scale(1.22)} 80%{transform:scale(1.08)} 100%{transform:scale(1.12);opacity:1} }
.picker-bottom { flex-shrink:0; padding:3px 8px 8px; display:flex; flex-direction:column; }
.preview-area { background:var(--white); border-radius:14px; padding:5px 7px 6px; box-shadow:0 -2px 14px rgba(0,0,0,.10),0 3px 10px rgba(0,0,0,.08); min-height:108px; display:flex; flex-direction:column; gap:3px; }
.preview-top-row { display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }
.preview-label { font-size:9px; font-weight:800; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
.preview-sel-badge { font-size:10px; font-weight:900; color:var(--orange); background:rgba(240,112,32,.1); border-radius:20px; padding:2px 8px; }
.preview-body { flex:1; display:flex; align-items:center; justify-content:center; gap:5px; }
.idle-block { display:flex; flex-direction:column; align-items:center; gap:3px; }
.idle-icon { font-size:22px; }
.idle-txt { font-size:9px; font-weight:800; color:var(--muted); text-align:center; line-height:1.4; }
.mini-card { flex:1; display:flex; flex-direction:column; gap:2px; min-width:0; }
.mini-card-title { text-align:center; font-size:8px; font-weight:900; color:var(--dark); }
.mini-hdr { display:grid; grid-template-columns:repeat(5,1fr); gap:1px; }
.mh { border-radius:3px; text-align:center; font-size:8px; font-weight:900; color:#fff; padding:1px 0; }
.mh.B{background:var(--red)} .mh.I{background:var(--amber)} .mh.N{background:var(--green)} .mh.G{background:var(--blue)} .mh.O{background:var(--purple)}
.mini-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:1px; flex:1; }
.mc { border-radius:3px; background:#ede8fd; display:flex; align-items:center; justify-content:center; font-family:'Nunito',sans-serif; font-size:clamp(5px,1.5vw,9px); font-weight:800; color:var(--dark); aspect-ratio:1; }
.mc.free { background:linear-gradient(135deg,var(--green),var(--green2)); color:#fff; }

/* ══════════════════════════════════
   SCREEN 3 — BINGO GAME
══════════════════════════════════ */
#screen-bingo { background:#cfc7f0; overflow-y:auto; overflow-x:hidden; }
.bingo-shell { width:100%; max-width:480px; min-height:100%; background:#b4a7df; padding:10px 8px 18px; display:flex; flex-direction:column; gap:8px; }
.status-bar { display:flex; align-items:center; gap:5px; }
.stat-box { flex:1; background:#fff; border:1.5px solid #9b7fd4; border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:5px 2px; min-width:0; }
.stat-label { font-size:9px; font-weight:700; color:#7c4dbb; text-transform:uppercase; letter-spacing:.3px; line-height:1.2; }
.stat-value { font-size:15px; font-weight:800; color:#222; line-height:1.2; font-family:'Nunito',sans-serif; }
.sound-btn { width:36px; height:36px; min-width:36px; border-radius:50%; background:#7c4dbb; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 8px rgba(124,77,187,.35); transition:transform .15s,background .2s; }
.sound-btn:hover { background:#5e3498; transform:scale(1.08); }
.sound-btn.muted { background:#aaa; }

.bingo-main { display:flex; gap:8px; align-items:flex-start; }
.number-board { background:rgba(255,255,255,.12); border-radius:14px; padding:7px 5px; flex-shrink:0; width:148px; }
.board-header { display:grid; grid-template-columns:repeat(5,1fr); gap:2px; margin-bottom:4px; }
.col-hdr { border-radius:6px; text-align:center; font-weight:900; font-size:13px; color:#fff; padding:3px 0; }
.col-hdr.b{background:#e8a020} .col-hdr.i{background:#2eaa5e} .col-hdr.n{background:#2871c9} .col-hdr.g{background:#c0302a} .col-hdr.o{background:#7c4dbb}
.board-grid { display:grid; grid-template-columns:repeat(5,1fr); grid-template-rows:repeat(15,1fr); grid-auto-flow:column; gap:2px; }
.board-cell { width:100%; aspect-ratio:1; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:rgba(255,255,255,.85); background:rgba(255,255,255,.18); cursor:default; transition:background .3s,color .3s,transform .25s,font-size .2s; user-select:none; }
.board-cell.called-current { background:#8B1A1A; color:#fff; box-shadow:0 0 10px rgba(139,26,26,.8); transform:scale(1.22); font-size:12px; z-index:2; position:relative; }
.board-cell.called-prev  { background:rgba(180,180,180,.55); color:#555; }
.board-cell.called-match { background:#2eaa5e; color:#fff; box-shadow:0 0 8px rgba(46,170,94,.6); }

.right-panel { flex:1; display:flex; flex-direction:column; gap:8px; min-width:0; }
.current-call-box { background:#6a3db8; border-radius:14px; display:flex; align-items:center; justify-content:space-between; padding:8px 10px 8px 14px; position:relative; min-height:70px; overflow:visible; flex-shrink:0; }
.current-call-left { display:flex; flex-direction:column; gap:2px; }
.current-call-label { color:#fff; font-size:14px; font-weight:700; letter-spacing:.5px; }
.countdown-wrap { display:flex; align-items:center; gap:5px; margin-top:4px; }
.countdown-bar-bg { width:90px; height:6px; background:rgba(255,255,255,.2); border-radius:3px; overflow:hidden; }
.countdown-bar-fill { height:100%; width:100%; background:#ffb347; border-radius:3px; transition:width 1s linear,background .5s; }
.countdown-bar-fill.urgent { background:#ff4444; }
.countdown-num { color:#fff; font-size:11px; font-weight:800; min-width:16px; text-align:right; opacity:.85; }
.call-ball { width:62px; height:62px; border-radius:50%; background:radial-gradient(circle at 35% 30%,#ffb347,#e07b00 60%,#b85c00); display:flex; align-items:center; justify-content:center; box-shadow:0 4px 16px rgba(200,100,0,.55),inset 0 -4px 8px rgba(0,0,0,.25),inset 0 4px 8px rgba(255,220,120,.45); position:absolute; right:-4px; top:50%; transform:translateY(-50%); z-index:10; }
.call-ball.pop { animation:ballPop .45s cubic-bezier(0.34,1.56,0.64,1); }
@keyframes ballPop { 0%{transform:translateY(-50%) scale(.55);opacity:.5} 65%{transform:translateY(-50%) scale(1.18)} 100%{transform:translateY(-50%) scale(1);opacity:1} }
#call-ball-text { color:#fff; font-size:15px; font-weight:900; text-shadow:0 1px 4px rgba(0,0,0,.4); letter-spacing:-.5px; }

.game-cartelas-stack { display:flex; flex-direction:column; gap:8px; }
.game-cartela-wrap { background:#fff; border-radius:14px; overflow:hidden; box-shadow:0 3px 14px rgba(80,40,160,.14); }
.game-cartela-title { text-align:center; font-size:12px; font-weight:600; color:#888; padding:5px 0 3px; background:#fafafa; }
.game-cartela-title em { color:var(--orange); font-style:normal; }
.game-cartela-hdr { display:grid; grid-template-columns:repeat(5,1fr); }
.gc-col { text-align:center; font-weight:900; font-size:13px; color:#fff; padding:5px 0; }
.gc-col.b{background:#e8a020} .gc-col.i{background:#2eaa5e} .gc-col.n{background:#2871c9} .gc-col.g{background:#c0302a} .gc-col.o{background:#7c4dbb}
.game-cartela-grid { display:grid; grid-template-columns:repeat(5,1fr); }
.gc-cell { display:flex; align-items:center; justify-content:center; aspect-ratio:1; font-size:14px; font-weight:700; color:#1a1a1a; background:#fff; border:.5px solid #eaeaea; cursor:pointer; transition:background .25s,color .25s,transform .2s; user-select:none; }
.gc-cell:active { transform:scale(.92); }
.gc-cell.free   { background:#2eaa5e; color:#fff; font-size:18px; cursor:default; }
.gc-cell.matched{ background:#2eaa5e; color:#fff; animation:matchFlash .5s ease; }
.gc-cell.manually-marked { background:#a78bfa; color:#fff; }
@keyframes matchFlash { 0%{background:#fff;transform:scale(1)} 40%{background:#a8edbe;transform:scale(1.12)} 100%{background:#2eaa5e;transform:scale(1)} }

.bingo-footer { display:flex; flex-direction:column; align-items:center; gap:8px; padding:0 2px; }
.bingo-btn { width:100%; padding:15px 0; border:none; border-radius:14px; background:#e8b89a; color:#fff; font-size:20px; font-weight:900; letter-spacing:3px; cursor:pointer; box-shadow:0 3px 12px rgba(200,120,80,.28); transition:background .2s,transform .15s; }
.bingo-btn:hover { background:#d9956e; transform:translateY(-1px); }
.bingo-btn.winner { background:linear-gradient(135deg,#f7b733,#fc4a1a); animation:winnerPulse .7s infinite alternate; }
@keyframes winnerPulse { from{box-shadow:0 0 12px rgba(247,183,51,.5)} to{box-shadow:0 0 32px rgba(252,74,26,.8)} }
.leave-link { font-size:14px; color:#5a3a9a; text-decoration:underline; cursor:pointer; font-weight:500; }

.win-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.55); z-index:999; align-items:center; justify-content:center; }
.win-overlay.active { display:flex; }
.win-box { background:#fff; border-radius:22px; padding:36px 40px; text-align:center; box-shadow:0 12px 48px rgba(0,0,0,.35); animation:winBoxIn .4s cubic-bezier(0.34,1.56,0.64,1); }
@keyframes winBoxIn { from{transform:scale(.5);opacity:0} to{transform:scale(1);opacity:1} }
.win-box h2 { font-size:36px; font-weight:900; color:#e07b00; margin-bottom:10px; }
.win-box p  { font-size:15px; color:#555; margin-bottom:20px; }
.win-close  { background:#6a3db8; color:#fff; border:none; border-radius:10px; padding:10px 28px; font-size:15px; font-weight:700; cursor:pointer; }

@media (max-width:360px) {
  .number-board { width:130px; }
  .board-cell { font-size:9px; }
  .gc-cell { font-size:12px; }
  .stat-value { font-size:13px; }
}
</style>
</head>
<body>

<!-- SCREEN 1 — LOBBY -->
<div id="screen-lobby" class="screen">
<div class="shell">
  <div class="top-row">
    <div class="top-card">
      <div class="ic ic-w">
        <svg viewBox="0 0 24 24" fill="none">
          <rect x="2" y="6" width="20" height="14" rx="3" fill="#f07020" opacity="0.12"/>
          <rect x="2" y="6" width="20" height="14" rx="3" stroke="#f07020" stroke-width="1.8"/>
          <circle cx="17" cy="13" r="1.2" fill="#f07020"/>
          <path d="M2 10h20" stroke="#f07020" stroke-width="1.8"/>
          <path d="M6 6V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1" stroke="#f07020" stroke-width="1.8"/>
        </svg>
      </div>
      <div>
        <div class="tlbl">Balance</div>
        <div class="tval" id="bal">100 ETB</div>
      </div>
    </div>
    <div class="top-card" onclick="refreshLobby()">
      <div class="ic ic-r">
        <svg id="ri" viewBox="0 0 24 24" fill="none">
          <path d="M4 12a8 8 0 0 1 13.66-5.66L20 9" stroke="#6c63d4" stroke-width="2" stroke-linecap="round"/>
          <path d="M20 4v5h-5" stroke="#6c63d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M20 12a8 8 0 0 1-13.66 5.66L4 15" stroke="#6c63d4" stroke-width="2" stroke-linecap="round"/>
          <path d="M4 20v-5h5" stroke="#6c63d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div class="tlbl">Update</div>
        <div class="tval sm">Refresh</div>
      </div>
    </div>
  </div>
  <div class="lobby-box">
    <div class="lhdr">
      <div class="hcol">Stake</div><div class="hcol">Active</div><div class="hcol">Players</div><div class="hcol">Derash</div><div class="hcol">Play</div>
    </div>
    <div class="l-rows" id="lobby-rows"></div>
  </div>
</div>
</div>

<!-- SCREEN 2 — CARTELA PICKER -->
<div id="screen-cartela" class="screen hidden">
<div class="picker-shell">
  <div class="picker-header">
    <button class="back-btn" onclick="pickerBack()">
      <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
        <path d="M15 18l-6-6 6-6" stroke="#2d2b6b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="hcard"><div class="lbl">Wallet</div><div class="val wallet-val" id="pickerWallet">100 ETB</div></div>
    <div class="hcard"><div class="lbl">Stake</div><div class="val stake-val" id="pickerStake">10 ETB</div></div>
    <div class="hcard cd-card"><div class="lbl">Starts in</div><div class="val" id="pickerCountdown">20s</div></div>
  </div>
  <div class="pool-scroll"><div class="pool-grid" id="poolGrid"></div></div>
  <div class="picker-bottom">
    <div class="preview-area">
      <div class="preview-top-row">
        <span class="preview-label">Cartela Preview</span>
        <span class="preview-sel-badge" id="previewBadge">0 / 2 selected</span>
      </div>
      <div class="preview-body" id="previewBody">
        <div class="idle-block"><div class="idle-icon">🎯</div><div class="idle-txt">Choose your Cartela</div></div>
      </div>
    </div>
  </div>
</div>
</div>

<!-- SCREEN 3 — BINGO GAME -->
<div id="screen-bingo" class="screen hidden">
<div class="bingo-shell">
  <div class="status-bar">
    <div class="stat-box"><span class="stat-label">Bet</span><span class="stat-value" id="gameBet">—</span></div>
    <div class="stat-box"><span class="stat-label">Derash</span><span class="stat-value" id="gameDerash">—</span></div>
    <div class="stat-box"><span class="stat-label">Players</span><span class="stat-value" id="gamePlayers">—</span></div>
    <div class="stat-box"><span class="stat-label">Call</span><span class="stat-value" id="gameCallCount">0</span></div>
    <button class="sound-btn" id="soundBtn"><svg viewBox="0 0 24 24" fill="white" width="20" height="20"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/></svg></button>
  </div>
  <div class="bingo-main">
    <div class="number-board">
      <div class="board-header"><div class="col-hdr b">B</div><div class="col-hdr i">I</div><div class="col-hdr n">N</div><div class="col-hdr g">G</div><div class="col-hdr o">O</div></div>
      <div class="board-grid" id="boardGrid"></div>
    </div>
    <div class="right-panel">
      <div class="current-call-box">
        <div class="current-call-left">
          <span class="current-call-label">Current Call</span>
          <div class="countdown-wrap">
            <div class="countdown-bar-bg"><div class="countdown-bar-fill" id="countdownFill"></div></div>
            <span class="countdown-num" id="countdownNum">5</span>
          </div>
        </div>
        <div class="call-ball" id="callBall"><span id="callBallText">—</span></div>
      </div>
      <div class="game-cartelas-stack" id="gameCartelasStack"></div>
    </div>
  </div>
  <div class="bingo-footer">
    <button class="bingo-btn" id="bingoBtn">BINGO!</button>
    <span class="leave-link" onclick="leaveGame()">Leave Game</span>
  </div>
</div>
</div>

<!-- WIN OVERLAY -->
<div class="win-overlay" id="winOverlay">
  <div class="win-box"><h2>🎉 BINGO!</h2><p>Congratulations! You won!</p><button class="win-close" id="winClose">Back to Lobby</button></div>
</div>

<script>
// ============================================================
// ANDROMEDA BINGO - Complete Working Version
// ============================================================

// STATE
let currentBalance = 100;
let currentStake = 0;
let currentGameId = '';
let currentPlayers = 0;
let currentPrizePool = 0;

let selectedCartelas = [];
let gameCartelas = [];
let gameCallCount = 0;
let gameNumbersLeft = [];
let gameInterval = null;
let gameCountdownInterval = null;
let gameSecondsLeft = 5;
let gameOver = false;
let soundEnabled = true;
let audioCtx = null;

// LOBBY DATA
let lobbyGames = [
  { id: 'game_10', stake: 10, players: 140, status: 'lobby', countdown: 18, prizePool: 1400 },
  { id: 'game_20', stake: 20, players: 102, status: 'lobby', countdown: 11, prizePool: 2040 },
  { id: 'game_50', stake: 50, players: 90, status: 'playing', countdown: 0, prizePool: 4500 }
];

// Helper Functions
function formatNumber(n) { return n.toLocaleString('en-US'); }
function getColLetter(n) { if(n<=15) return 'B'; if(n<=30) return 'I'; if(n<=45) return 'N'; if(n<=60) return 'G'; return 'O'; }

// Generate Cartela (seeded by ID)
function generateCartela(seed) {
  let s = (seed ^ 0x9e3779b9) >>> 0;
  const rng = () => { s = Math.imul(s ^ (s >>> 15), 0x2c1b3c6d) | 0; s = Math.imul(s ^ (s >>> 12), 0x297a2153) | 0; s = (s ^ (s >>> 13)) >>> 0; return s / 0x100000000; };
  const ranges = [[1,15],[16,30],[31,45],[46,60],[61,75]];
  const cols = ranges.map(([lo,hi]) => { let pool=[]; for(let n=lo;n<=hi;n++) pool.push(n); for(let i=pool.length-1;i>0;i--){let j=Math.floor(rng()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]];} return pool.slice(0,5); });
  let grid = [];
  for(let r=0;r<5;r++) grid.push(cols.map(c=>c[r]));
  grid[2][2] = 'FREE';
  return grid;
}

// SCREEN NAVIGATION
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
}

// LOBBY RENDER
function renderLobby() {
  const container = document.getElementById('lobby-rows');
  container.innerHTML = '';
  lobbyGames.forEach(game => {
    const isLobby = game.status === 'lobby';
    const statusHtml = isLobby ? `<span class="b-timer${game.countdown<=5 ? ' urg' : ''}" id="timer-${game.id}">${game.countdown}s</span>` : 
                       (game.status === 'playing' ? '<span class="b-playing">playing</span>' : '<span class="b-finished">Finished</span>');
    const btnHtml = isLobby ? `<button class="btn-play" onclick="joinGame('${game.id}')">Play</button>` : 
                             `<button class="btn-disabled" disabled>Playing</button>`;
    const row = document.createElement('div');
    row.className = 'row-outer';
    row.innerHTML = `
      <div class="badge"><span class="bdot"></span>Active game</div>
      <div class="grow">
        <div class="lstake">${game.stake} ETB</div>
        <div class="lscell">${statusHtml}</div>
        <div class="lpcell" id="players-${game.id}">${formatNumber(game.players)}</div>
        <div class="ldcell" id="prize-${game.id}">${formatNumber(game.prizePool)} ETB<small>Prize Pool</small></div>
        <div class="lplaycell">${btnHtml}</div>
      </div>`;
    container.appendChild(row);
  });
}

function refreshLobby() {
  lobbyGames.forEach(g => { if(g.status === 'lobby') { g.players += Math.floor(Math.random() * 5) + 1; g.prizePool = g.players * g.stake; } });
  renderLobby();
}

// LOBBY TICK
setInterval(() => {
  let needRender = false;
  lobbyGames.forEach(g => {
    if(g.status === 'lobby') {
      g.countdown--;
      const el = document.getElementById(`timer-${g.id}`);
      if(el) { el.textContent = `${g.countdown}s`; if(g.countdown<=5) el.classList.add('urg'); }
      if(g.countdown <= 0) { g.status = 'playing'; needRender = true; }
    } else if(g.status === 'playing') {
      // Auto-finish after 60 seconds (simulated)
      if(Math.random() < 0.02) { g.status = 'finished'; needRender = true; }
    } else if(g.status === 'finished') {
      // Reset after 10 seconds
      if(!g.resetTimer) { g.resetTimer = 10; }
      g.resetTimer--;
      if(g.resetTimer <= 0) {
        g.status = 'lobby';
        g.countdown = 20;
        g.players = 60 + Math.floor(Math.random() * 80);
        g.prizePool = g.players * g.stake;
        delete g.resetTimer;
        needRender = true;
      }
    }
  });
  if(needRender) renderLobby();
}, 1000);

// JOIN GAME
async function joinGame(gameId) {
  const game = lobbyGames.find(g => g.id === gameId);
  if(!game || game.status !== 'lobby') return;
  currentStake = game.stake;
  currentGameId = gameId;
  currentPlayers = game.players;
  currentPrizePool = game.prizePool;
  game.status = 'playing';
  renderLobby();
  openPicker();
}

function openPicker() {
  document.getElementById('pickerWallet').textContent = currentBalance + ' ETB';
  document.getElementById('pickerStake').textContent = currentStake + ' ETB';
  selectedCartelas = [];
  renderPickerGrid();
  updatePreview();
  startPickerCountdown();
  showScreen('screen-cartela');
}

function renderPickerGrid() {
  const grid = document.getElementById('poolGrid');
  grid.innerHTML = '';
  for(let n=1; n<=400; n++) {
    const cell = document.createElement('div');
    cell.className = 'pool-cell';
    cell.textContent = n;
    cell.onclick = () => toggleCartelaSelect(n);
    grid.appendChild(cell);
  }
}

function toggleCartelaSelect(num) {
  const idx = selectedCartelas.indexOf(num);
  const cell = document.querySelector(`#poolGrid .pool-cell:nth-child(${num})`);
  if(idx === -1) {
    if(selectedCartelas.length >= 2) return;
    selectedCartelas.push(num);
    cell.classList.add('active');
  } else {
    selectedCartelas.splice(idx,1);
    cell.classList.remove('active');
  }
  updatePreview();
  document.getElementById('previewBadge').textContent = `${selectedCartelas.length} / 2 selected`;
}

function updatePreview() {
  const body = document.getElementById('previewBody');
  if(selectedCartelas.length === 0) {
    body.innerHTML = '<div class="idle-block"><div class="idle-icon">🎯</div><div class="idle-txt">Choose your Cartela</div></div>';
    return;
  }
  body.innerHTML = '';
  selectedCartelas.forEach(id => {
    const grid = generateCartela(id);
    const card = document.createElement('div');
    card.className = 'mini-card';
    card.innerHTML = `
      <div class="mini-card-title">Cartela #<em>${id}</em></div>
      <div class="mini-hdr"><div class="mh B">B</div><div class="mh I">I</div><div class="mh N">N</div><div class="mh G">G</div><div class="mh O">O</div></div>
      <div class="mini-grid">${grid.flat().map(v => v==='FREE' ? '<div class="mc free">★</div>' : `<div class="mc">${v}</div>`).join('')}</div>
    `;
    body.appendChild(card);
  });
}

let pickerTimer = null;
let pickerCd = 20;

function startPickerCountdown() {
  if(pickerTimer) clearInterval(pickerTimer);
  pickerCd = 20;
  updatePickerDisplay();
  pickerTimer = setInterval(() => {
    pickerCd--;
    updatePickerDisplay();
    if(pickerCd <= 0) { clearInterval(pickerTimer); startGame(); }
  }, 1000);
}

function updatePickerDisplay() {
  const el = document.getElementById('pickerCountdown');
  if(el) { el.textContent = pickerCd + 's'; if(pickerCd<=5) el.classList.add('urg'); else el.classList.remove('urg'); }
}

function pickerBack() {
  if(pickerTimer) clearInterval(pickerTimer);
  showScreen('screen-lobby');
}

// START BINGO GAME
function startGame() {
  if(pickerTimer) clearInterval(pickerTimer);
  if(selectedCartelas.length === 0) selectedCartelas = [Math.floor(Math.random()*400)+1];
  gameCartelas = selectedCartelas.map(id => ({ id, grid: generateCartela(id), matched: new Set(), manual: new Set() }));
  document.getElementById('gameBet').textContent = currentStake;
  document.getElementById('gameDerash').textContent = formatNumber(currentPrizePool);
  document.getElementById('gamePlayers').textContent = formatNumber(currentPlayers);
  buildBoard();
  buildGameCartelas();
  resetBingoGame();
  showScreen('screen-bingo');
  setTimeout(() => { startBingo(); }, 500);
}

function buildBoard() {
  const grid = document.getElementById('boardGrid');
  grid.innerHTML = '';
  for(let n=1; n<=75; n++) {
    const cell = document.createElement('div');
    cell.className = 'board-cell';
    cell.textContent = n;
    cell.id = `boardCell_${n}`;
    grid.appendChild(cell);
  }
}

function buildGameCartelas() {
  const stack = document.getElementById('gameCartelasStack');
  stack.innerHTML = '';
  gameCartelas.forEach((cart, idx) => {
    const wrap = document.createElement('div');
    wrap.className = 'game-cartela-wrap';
    wrap.innerHTML = `
      <div class="game-cartela-title">Cartela #<em>${cart.id}</em></div>
      <div class="game-cartela-hdr"><div class="gc-col b">B</div><div class="gc-col i">I</div><div class="gc-col n">N</div><div class="gc-col g">G</div><div class="gc-col o">O</div></div>
      <div class="game-cartela-grid" id="cartelaGrid_${idx}"></div>
    `;
    stack.appendChild(wrap);
    renderCartelaGrid(idx, cart);
  });
}

function renderCartelaGrid(idx, cart) {
  const gridDiv = document.getElementById(`cartelaGrid_${idx}`);
  gridDiv.innerHTML = '';
  cart.grid.forEach(row => {
    row.forEach(val => {
      const cell = document.createElement('div');
      if(val === 'FREE') {
        cell.className = 'gc-cell free';
        cell.textContent = '★';
      } else {
        cell.className = 'gc-cell';
        cell.textContent = val;
        const isMatched = cart.matched.has(val);
        const isManual = cart.manual.has(val);
        if(isMatched && !isManual) cell.classList.add('matched');
        else if(isManual) cell.classList.add('manually-marked');
        cell.onclick = () => toggleManualMark(idx, val);
      }
      gridDiv.appendChild(cell);
    });
  });
}

function toggleManualMark(cartIdx, num) {
  const cart = gameCartelas[cartIdx];
  if(cart.matched.has(num) && !cart.manual.has(num)) {
    cart.manual.add(num);
    cart.matched.delete(num);
  } else if(cart.manual.has(num)) {
    cart.manual.delete(num);
    if(cart.matched.has(num)) cart.matched.add(num);
  } else if(!cart.matched.has(num)) {
    cart.manual.add(num);
  }
  renderCartelaGrid(cartIdx, cart);
}

function resetBingoGame() {
  gameCallCount = 0;
  gameNumbersLeft = [];
  for(let i=1;i<=75;i++) gameNumbersLeft.push(i);
  document.getElementById('gameCallCount').textContent = '0';
  document.getElementById('callBallText').textContent = '—';
  document.getElementById('countdownFill').style.width = '100%';
  document.getElementById('countdownNum').textContent = '5';
  gameOver = false;
  gameSecondsLeft = 5;
  document.getElementById('bingoBtn').classList.remove('winner');
  gameCartelas.forEach(c => { c.matched.clear(); c.manual.clear(); });
  gameCartelas.forEach((_,idx) => renderCartelaGrid(idx, gameCartelas[idx]));
  document.querySelectorAll('.board-cell').forEach(cell => { cell.classList.remove('called-current','called-prev','called-match'); });
}

function startBingo() {
  if(gameInterval) clearInterval(gameInterval);
  if(gameCountdownInterval) clearInterval(gameCountdownInterval);
  gameInterval = setInterval(callNumber, 5000);
  gameCountdownInterval = setInterval(tickCountdown, 1000);
  gameSecondsLeft = 5;
  updateCountdownDisplay();
}

function tickCountdown() {
  if(gameOver) return;
  gameSecondsLeft = Math.max(0, gameSecondsLeft - 1);
  updateCountdownDisplay();
}

function updateCountdownDisplay() {
  const fill = document.getElementById('countdownFill');
  const num = document.getElementById('countdownNum');
  if(fill) fill.style.width = (gameSecondsLeft / 5 * 100) + '%';
  if(num) num.textContent = gameSecondsLeft;
  if(fill && gameSecondsLeft <= 2) fill.classList.add('urgent');
  else if(fill) fill.classList.remove('urgent');
}

function resetCountdown() {
  clearInterval(gameCountdownInterval);
  gameSecondsLeft = 5;
  updateCountdownDisplay();
  gameCountdownInterval = setInterval(tickCountdown, 1000);
}

function callNumber() {
  if(gameNumbersLeft.length === 0 || gameOver) { stopBingo(); return; }
  const idx = Math.floor(Math.random() * gameNumbersLeft.length);
  const num = gameNumbersLeft.splice(idx,1)[0];
  const col = getColLetter(num);
  gameCallCount++;
  document.getElementById('gameCallCount').textContent = gameCallCount;
  
  // Animate ball
  const ball = document.getElementById('callBall');
  ball.classList.remove('pop'); void ball.offsetWidth; ball.classList.add('pop');
  document.getElementById('callBallText').textContent = col + num;
  
  // Update board
  document.querySelectorAll('.board-cell.called-current').forEach(c => {
    const n = parseInt(c.id.replace('boardCell_',''));
    const hasMatch = gameCartelas.some(cart => cart.grid.flat().includes(n));
    c.classList.remove('called-current');
    c.classList.add(hasMatch ? 'called-match' : 'called-prev');
  });
  const boardCell = document.getElementById(`boardCell_${num}`);
  if(boardCell) { boardCell.classList.remove('called-prev','called-match'); boardCell.classList.add('called-current'); }
  
  // Auto-match
  let bingoFound = false;
  gameCartelas.forEach((cart, cartIdx) => {
    const hasNum = cart.grid.flat().includes(num);
    if(hasNum && !cart.manual.has(num)) {
      cart.matched.add(num);
      renderCartelaGrid(cartIdx, cart);
    }
    if(checkBingo(cart) && !bingoFound) bingoFound = true;
  });
  
  if(bingoFound) triggerBingo();
  if(soundEnabled) playSound();
  resetCountdown();
}

function checkBingo(cart) {
  for(let r=0;r<5;r++) if([0,1,2,3,4].every(c => { const v=cart.grid[r][c]; return v==='FREE' || (cart.matched.has(v) && !cart.manual.has(v)); })) return true;
  for(let c=0;c<5;c++) if([0,1,2,3,4].every(r => { const v=cart.grid[r][c]; return v==='FREE' || (cart.matched.has(v) && !cart.manual.has(v)); })) return true;
  if([0,1,2,3,4].every(i => { const v=cart.grid[i][i]; return v==='FREE' || (cart.matched.has(v) && !cart.manual.has(v)); })) return true;
  if([0,1,2,3,4].every(i => { const v=cart.grid[i][4-i]; return v==='FREE' || (cart.matched.has(v) && !cart.manual.has(v)); })) return true;
  return false;
}

function triggerBingo() {
  gameOver = true;
  stopBingo();
  document.getElementById('bingoBtn').classList.add('winner');
  document.getElementById('winOverlay').classList.add('active');
  currentBalance += currentPrizePool * 0.8;
}

function stopBingo() {
  if(gameInterval) clearInterval(gameInterval);
  if(gameCountdownInterval) clearInterval(gameCountdownInterval);
  gameInterval = null;
  gameCountdownInterval = null;
}

function leaveGame() {
  stopBingo();
  document.getElementById('winOverlay').classList.remove('active');
  showScreen('screen-lobby');
}

// BINGO BUTTON
document.getElementById('bingoBtn').addEventListener('click', () => {
  if(gameCartelas.some(c => checkBingo(c))) triggerBingo();
});

document.getElementById('winClose').addEventListener('click', () => {
  document.getElementById('winOverlay').classList.remove('active');
  leaveGame();
});

// SOUND
document.getElementById('soundBtn').addEventListener('click', () => {
  soundEnabled = !soundEnabled;
  document.getElementById('soundBtn').classList.toggle('muted', !soundEnabled);
});

function playSound() {
  try {
    if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(660, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.12);
    gain.gain.setValueAtTime(0.18, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + 0.36);
  } catch(e) {}
}

// INIT
renderLobby();
</script>
</body>
</html>