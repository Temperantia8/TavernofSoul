cd /home/temperantia/TavernofSoul/
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
# ========== downloading patch ipf ========
cd downloader
python downloader.py itos
cd ..
# ========== unpacking ipf ========
# python unpackIPF.py itos  # included in downloader
# ========== parsing unpacked ipf ========
cd parser_tidy
source /home/temperantia/TavernofSoul/py27/bin/activate
python map_image.py itos
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
python main.py itos
# ========== importing changes to DB ========
cd ..
cd TavernofSoul
python manage_itos.py importAll >> ../err.txt
cd ..
python closer.py itos
