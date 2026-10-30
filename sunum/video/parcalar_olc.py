"""Slayt içindeki parçaların (satır, çubuk, yazı aralığı, resim) yerini headless Chrome ile ölçer (CSS pikseli, 1920x1080 slayt).
Çalıştırma (proje klasöründen): python sunum/video/parcalar_olc.py  (slaytlar ONIZLEME=1 slayt_uret.py ile, headless Chrome)
Çıktı: sunum/video/parcalar.json (gostergeler_zaman.py okur)  {sayfa: {ad: {x,y,w,h}}, "_img": {sayfa: [{src,x,y,w,h,nw,nh}]}}"""
import json, os, subprocess, sys, tempfile, shutil, re
from pathlib import Path
KOK = Path("/Users/yazelsudeozyurek/asa data python")
BURA = Path(__file__).parent  # çıktı: sunum/video/parcalar.json
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = ('<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">')
CSS = ("*{margin:0;box-sizing:border-box} body{margin:0} section{position:relative;width:1920px;height:1080px;overflow:hidden} "
       "aside{display:none} section > *:not([style*=\"position:absolute\"]){position:relative}")
# ("metin", aralık) = yazı aralığının kutusu; ("oge", [parçalar]) = hepsini içeren en küçük öğe
OLC = {
 "question": {
   "kanca_kore": ("oge", ["0.72", "Korea"]), "kanca_nijer": ("oge", ["6.06", "Niger"]),
   "q1": ("metin", "Q1 Same path, only different timing?"), "q2": ("metin", "Q2 Income or education?"),
   "q3": ("metin", "Q3 Health first?"),
   "huni_555": ("oge", ["555 rows", "362.9"]), "huni_237": ("oge", ["237", "8.09"]), "huni_200": ("oge", ["200", "99.98"]),
   "dip_veri": ("metin", "UN World Population Prospects 2024"),
   "dip_liste": ("metin", "every excluded place is listed by name (excluded_places.csv)"),
 },
 "clock": {
   "r2_ayri": ("oge", ["Separate curves", "0.99"]), "r2_takvim": ("oge", ["Calendar year only", "0.27"]),
   "r2_zaman": ("oge", ["Curve + time shift", "0.94"]),
   "bt_shared": ("oge", ["Shared"]), "bt_049": ("oge", ["0.49"]), "bt_038": ("oge", ["0.38"]), "bt_041": ("oge", ["0.41"]),
   "dip_sitar": ("metin", "After SITAR growth curves (Cole et al., 2010)"),
   "dip_16": ("metin", "* 16 of 200 separate fits hit their limits"),
   "alt_egri": ("metin", "one shared S-curve, one time shift (turning point) per country"),
 },
 "money": {
   "hata_gelir": ("oge", ["Income", "14.0"]), "hata_okul": ("oge", ["Schooling", "9.5"]), "hata_takvim": ("oge", ["Calendar", "9.5"]),
   "yer_gelir": ("oge", ["$1,096", "no wealth threshold"]), "yer_okul": ("oge", ["Schooling", "tighter"]),
   "alt_q3": ("metin", "Q3 Health first? 115 countries, UN WPP"),
   "dip_tarama": ("metin", "many other candidates screened (FDR)"),
   "dip_neden": ("metin", "association, not cause"),
 },
 "turkiye": {
   "alt_q4": ("metin", "Q4 Is health a cause?"),
   "testler": ("oge", ["Three tests", "Fertility fall"]),
   "cip_timing": ("oge", ["Timing", "F < 1"]), "cip_hiv": ("oge", ["HIV shock"]), "cip_fert": ("oge", ["Fertility fall"]),
   "satir_10": ("oge", ["About 10% more life expectancy", "fewer children"]),
   "iddia_neden": ("oge", ["A settled cause"]), "iddia_birey": ("oge", ["Individual-level facts"]),
   "iddia_yaris": ("oge", ["That ahead is better"]),
   "tr_baslik": ("oge", ["Türkiye: health 1965"]),
 },
}
JS = r"""
<script>
const OLC = __OLC__;
function birlesim(rs){ rs=[...rs].filter(r=>r.width>0&&r.height>0); if(!rs.length) return null;
  const x0=Math.min(...rs.map(r=>r.left)), y0=Math.min(...rs.map(r=>r.top)), x1=Math.max(...rs.map(r=>r.right)), y1=Math.max(...rs.map(r=>r.bottom));
  return {x:x0,y:y0,w:x1-x0,h:y1-y0}; }
function metin(sub){
  const w=document.createTreeWalker(document.querySelector('section'),NodeFilter.SHOW_TEXT); const ds=[]; let tam='';
  while(w.nextNode()){ const n=w.currentNode; if(n.parentElement.closest('aside')) continue; ds.push([n,tam.length]); tam+=n.data; }
  const i=tam.indexOf(sub); if(i<0) return 'YOK'; if(tam.indexOf(sub,i+1)>=0) return 'COK';
  const bul=k=>{ for(let j=ds.length-1;j>=0;j--) if(ds[j][1]<=k) return [ds[j][0],k-ds[j][1]]; };
  const r=document.createRange(); const [a,ao]=bul(i), [b,bo]=bul(i+sub.length-1); r.setStart(a,ao); r.setEnd(b,bo+1);
  return birlesim(r.getClientRects()); }
function oge(subs){ let en=null;
  document.querySelectorAll('section *').forEach(e=>{ if(e.closest('aside')) return; const t=e.textContent;
    if(subs.every(s=>t.includes(s))){ const r=e.getBoundingClientRect(), a=r.width*r.height; if(a>0&&(!en||a<en.a)) en={a,r,e}; }});
  if(!en) return 'YOK'; const e=en.e, rs=[];
  const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); while(w.nextNode()){const n=w.currentNode; if(!n.data.trim()) continue; const r=document.createRange(); r.selectNodeContents(n); rs.push(...r.getClientRects());}
  [e,...e.querySelectorAll('*')].forEach(d=>{const cs=getComputedStyle(d); if(cs.backgroundColor!=='rgba(0, 0, 0, 0)'||cs.backgroundImage!=='none'||parseFloat(cs.borderTopWidth)>0) rs.push(d.getBoundingClientRect());});
  return birlesim(rs); }
window.addEventListener('load',()=>setTimeout(()=>{ const out={};
  for(const [ad,[tur,arg]] of Object.entries(OLC)) out[ad]= tur==='metin'?metin(arg):oge(arg);
  out._img=[...document.querySelectorAll('section img')].map(i=>{const r=i.getBoundingClientRect(); return {src:i.getAttribute('src'),x:r.left,y:r.top,w:r.width,h:r.height,nw:i.naturalWidth,nh:i.naturalHeight};});
  const p=document.createElement('pre'); p.id='olcum'; p.textContent=JSON.stringify(out); document.body.appendChild(p); },1500));
</script>"""
gecici = Path(tempfile.mkdtemp(prefix="odak_"))
sonuc = {}
try:
    subprocess.run([sys.executable, str(KOK / "sunum/slayt_uret.py"), str(gecici)], check=True, env={**os.environ, "ONIZLEME": "1"}, cwd=KOK)
    for ad, olc in OLC.items():
        sayfa = gecici / f"{ad}_olc.html"
        sayfa.write_text(f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{CSS}</style></head><body>"
                         + (gecici / f"{ad}.html").read_text(encoding="utf-8")
                         + JS.replace("__OLC__", json.dumps(olc, ensure_ascii=False)) + "</body></html>", encoding="utf-8")
        profil = tempfile.mkdtemp(prefix="odak_chrome_")
        try:
            r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                                f"--user-data-dir={profil}", "--window-size=1920,1080", "--virtual-time-budget=8000",
                                "--dump-dom", sayfa.as_uri()], capture_output=True, text=True, timeout=180, check=True)
        finally:
            shutil.rmtree(profil, ignore_errors=True)
        m = re.search(r'<pre id="olcum">(.*?)</pre>', r.stdout, re.S)
        d = json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
        sonuc[ad] = d
        for k, v in d.items():
            if k != "_img": print(ad, k, v if isinstance(v, str) else {a: round(b, 1) for a, b in v.items()})
        for i in d["_img"]: print(ad, "img", Path(i["src"]).name, {a: round(i[a], 1) for a in "xywh"}, i["nw"], i["nh"])
finally:
    shutil.rmtree(gecici, ignore_errors=True)
(BURA / "parcalar.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1))
