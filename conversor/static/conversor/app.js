const $ = id => document.getElementById(id);
const numEl = $('num'), baseEl = $('base');
let bitWidth = 8, datos = null, peticion = 0, timer = null;

const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

async function convertir() {
  const id = ++peticion;
  const params = new URLSearchParams({valor: numEl.value, base: baseEl.value, ancho: bitWidth});
  const resp = await fetch(`${API_URL}?${params}`);
  const json = await resp.json();
  if (id !== peticion) return;
  if (json.error) {
    numEl.classList.add('bad');
    $('msg').textContent = '⚠ ' + json.error;
    return;
  }
  numEl.classList.remove('bad');
  $('msg').textContent = '';
  datos = json.datos;
  render();
}
const convertirPronto = () => { clearTimeout(timer); timer = setTimeout(convertir, 120); };

function render() {
  if (!datos) { ['results', 'bits', 'info', 'widths'].forEach(i => $(i).innerHTML = ''); $('bitinfo').textContent = ''; return; }
  $('results').innerHTML = datos.resultados.map(r => {
    const tag = `<span class="tag">${esc(r.etiqueta)}</span>`;
    return `<div class="card res" style="--c:${r.color}" data-copy="${esc(r.valor)}">
      <div class="top"><span class="name">${esc(r.nombre)}</span>${tag}</div>
      <div class="val">${esc(r.valor)}</div><div class="hint">${esc(r.pista)}</div></div>`;
  }).join('');

  const b = datos.bits;
  bitWidth = b.ancho;
  $('widths').innerHTML = [8, 16, 32, 64].map(w => `<button class="chip ${w === b.ancho ? 'active' : ''}" data-w="${w}">${w} bits</button>`).join('');
  let html = '';
  for (let i = 0; i < b.ancho; i += 8) {
    html += '<div class="byte">';
    for (let j = i; j < i + 8; j++) {
      const pos = b.ancho - 1 - j;
      html += `<div class="bit ${b.cadena[j] === '1' ? 'on' : ''}" data-p="${pos}" title="bit ${pos} = 2^${pos}">${b.cadena[j]}</div>`;
    }
    html += '</div>';
  }
  $('bits').innerHTML = html;
  $('bitinfo').textContent = `${b.ancho} bits · ${b.unos} unos · ${b.ancho - b.unos} ceros${b.complemento_a_2 ? ' · complemento a 2' : ''}`;
  $('info').innerHTML = datos.info.map(([k, v]) => `<div class="stat"><span>${esc(k)}</span><b>${esc(v)}</b></div>`).join('');
}

function aBase(v, base) {
  return (v < 0n ? '-' : '') + (v < 0n ? -v : v).toString(base).toUpperCase();
}

$('bits').addEventListener('click', e => {
  const el = e.target.closest('.bit');
  if (!el || !datos) return;
  const W = BigInt(datos.bits.ancho), p = BigInt(el.dataset.p);
  const actual = BigInt(datos.valor);
  let u = (actual < 0n ? (1n << W) + actual : actual) ^ (1n << p);
  if (actual < 0n && (u >> (W - 1n)) & 1n) u -= (1n << W);
  numEl.value = aBase(u, +baseEl.value);
  convertir();
});
$('widths').addEventListener('click', e => {
  const c = e.target.closest('[data-w]');
  if (!c) return;
  bitWidth = +c.dataset.w;
  convertir();
});
$('results').addEventListener('click', e => {
  const c = e.target.closest('.res');
  if (!c || !c.dataset.copy || c.dataset.copy === '—') return;
  navigator.clipboard?.writeText(c.dataset.copy).catch(() => {});
  const t = $('toast');
  t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 1200);
});
document.querySelectorAll('.chip[data-v]').forEach(c => c.addEventListener('click', () => {
  numEl.value = c.dataset.v; baseEl.value = c.dataset.b; bitWidth = 8; convertir();
}));
baseEl.addEventListener('change', () => {
  if (datos && !numEl.classList.contains('bad')) numEl.value = aBase(BigInt(datos.valor), +baseEl.value);
  convertir();
});
numEl.addEventListener('input', () => {
  bitWidth = 8;
  if (!numEl.value.trim()) { datos = null; peticion++; numEl.classList.remove('bad'); $('msg').textContent = ''; render(); return; }
  convertirPronto();
});
convertir();
