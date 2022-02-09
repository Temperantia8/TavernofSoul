cd /home/temperantia/All_TavernofSoul/
source /home/temperantia/All_TavernofSoul/TavernofSoul/itos/3.8/bin/activate
# ========== downloading patch ipf ========
cd downloader
python downloader.py jtos
cd ..
# ========== unpacking ipf ========
# python unpackIPF.py jtos
# ========== parsing unpacked ipf ========
cd parser_tidy
source /home/temperantia/All_TavernofSoul/py27/bin/activate
python map_image.py jtos
source /home/temperantia/All_TavernofSoul/TavernofSoul/itos/3.8/bin/activate
python main.py jtos
# ========== importing changes to DB ========
cd ..
cd TavernofSoul
python manage_jtos.py importAll >> ../err.txt
cd ..
python closer.py jtos
