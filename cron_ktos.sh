cd /home/temperantia/All_TavernofSoul/
source /home/temperantia/All_TavernofSoul/TavernofSoul/ktos/3.8/bin/activate
# ========== downloading patch ipf ========
cd downloader
python downloader.py ktos
cd ..
# ========== unpacking ipf ========
# python unpackIPF.py ktos
# ========== parsing unpacked ipf ========
cd parser_tidy
source /home/temperantia/All_TavernofSoul/py27/bin/activate
python map_image.py ktos
source /home/temperantia/All_TavernofSoul/TavernofSoul/ktos/3.8/bin/activate
python main.py ktos
# ========== importing changes to DB ========
cd ..
cd TavernofSoul
python manage_ktos.py importAll >> ../err.txt
cd ..
python closer.py ktos
python build_cache.py ktos