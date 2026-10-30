#!/bin/bash
# Teslim öncesi tam tekrar: README'deki "How to reproduce" 3. ve 4. adımları sırayla çalıştırır,
# sonra git ile hangi dosyaların değiştiğini gösterir (değişen yoksa her sayı aynı çıkmıştır).
# Kullanım (önce VS Code'da açık notebook sekmelerini kapat; sonra VS Code terminalinde, proje klasöründe):
#     bash tekrar_calistir.sh
# Notebook'lar zaten çalıştıysa sadece 4. adım:  bash tekrar_calistir.sh 4
# Süre: yaklaşık 15–30 dakika. Ayrıntılı ekran çıktısı: tekrar_log.txt
cd "$(dirname "$0")" || exit 1
PY=/opt/anaconda3/bin/python
LOG=tekrar_log.txt
HATA=0
adim() {   # adim "<ad>" komut ...
  echo "== $(date +%H:%M:%S)  $1" | tee -a "$LOG"; shift
  if ! "$@" >>"$LOG" 2>&1; then echo "   HATA: ayrıntı $LOG içinde" | tee -a "$LOG"; HATA=1; fi
}
echo "Başladı: $(date)" | tee "$LOG"

# 3) Notebook'lar, sırayla (her biri yeni bir çekirdekte baştan sona = Restart & Run All)
if [ "$1" != "4" ]; then
  for nb in 01_veriyi_tanima 02_temizlik 03_eda 04_demografik_saat 05_para_mi_okul_mu 06_final_grafikler; do
    adim "notebook $nb" bash -c "cd notebooks && $PY -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 $nb.ipynb"
  done
fi

# 4) Grafikler, testler ve slaytlar (README ile aynı sıra)
adim "pilot/slayt_grafikleri.py"   $PY pilot/slayt_grafikleri.py
adim "pilot/saglik_saati.py (Q3)"  $PY pilot/saglik_saati.py
adim "pilot/slayt_koyu.py"         $PY pilot/slayt_koyu.py
adim "pilot/harita_test.py"        $PY pilot/harita_test.py
adim "pilot/kapak_saat.py"         $PY pilot/kapak_saat.py
adim "pilot/animasyon.py"          env TEMA=koyu SADE=1 $PY pilot/animasyon.py
adim "pilot/ml_kontrol.py"         $PY pilot/ml_kontrol.py
adim "Q4 test 1 (d_neden)"         bash -c "$PY kesif/d_neden/neden_testi.py > kesif/d_neden/log.txt"
adim "Q4 test 2 (e_hiv)"           bash -c "$PY kesif/e_hiv/hiv_testi.py > kesif/e_hiv/log.txt"
adim "Q4 test 3 (f_kreitmeir)"     bash -c "$PY kesif/f_kreitmeir/ku_testi.py > kesif/f_kreitmeir/log.txt"
adim "Q4 sonradan kontroller"      bash -c "$PY kesif/f_kreitmeir/sonradan_kontrol.py > kesif/f_kreitmeir/log_sonradan.txt"
adim "pilot/neden_grafigi.py (Q4)" $PY pilot/neden_grafigi.py
adim "sunum/slayt_uret.py"         $PY sunum/slayt_uret.py sunum/slaytlar_kaynak/slides

echo "Bitti: $(date)" | tee -a "$LOG"
echo "--- git: değişen dosyalar (notebook'larda sadece zaman bilgisi değişir; Claude çıktıları ayrıca karşılaştıracak) ---" | tee -a "$LOG"
git status --short | tee -a "$LOG"
[ "$HATA" = 1 ] && echo "UYARI: en az bir adım hata verdi, tekrar_log.txt'ye bak." | tee -a "$LOG"
echo "Şimdi Claude'a 'bitti' yaz."
