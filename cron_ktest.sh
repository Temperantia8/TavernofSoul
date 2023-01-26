cd /home/temperantia/TavernofSoul/
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
# ========== downloading patch ipf ========
cd downloader
python downloader.py ktest
cd ..
# ========== unpacking ipf ========
# python unpackIPF.py ktest
# ========== parsing unpacked ipf ========
cd parser_tidy
source /home/temperantia/TavernofSoul/py27/bin/activate
python map_image.py ktest
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
python main.py ktest
# ========== importing changes to DB ========
cd ..
cd TavernofSoul
python manage_ktest.py importAll >> ../err.txt
cd ..
python closer.py ktest
