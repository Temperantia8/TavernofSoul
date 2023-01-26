cd /home/temperantia/TavernofSoul/
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
# ========== downloading patch ipf ========
cd downloader
python downloader.py twtos
cd ..
# ========== unpacking ipf ========
# python unpackIPF.py itos  # included in downloader
# ========== parsing unpacked ipf ========
cd parser_tidy
source /home/temperantia/TavernofSoul/py27/bin/activate
python map_image.py twtos
source /home/temperantia/TavernofSoul/TavernofSoul/itos/3.8/bin/activate
python main.py twtos
# ========== importing changes to DB ========
cd ..
cd TavernofSoul
python manage_twtos.py importAll >> ../err.txt
cd ..
python closer.py twtos
