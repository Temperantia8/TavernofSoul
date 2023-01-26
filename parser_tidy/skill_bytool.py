import logging
import glob
from DB import ToS_DB as constants
import xml.etree.ElementTree as ET
import os
import luautil
import codecs
test = 0
def parse(c):
    xml_skills = {}
    logging.debug('Parsing Monster Skill by Tool...')
    xml_pattern = os.path.join(c.PATH_INPUT_DATA, 'skill_bytool.ipf', '*.xml')
    flag = 1
    for path in glob.glob(xml_pattern):
        #if not flag:
        #    break
        try:
            with codecs.open(path,'r',encoding='utf-8',errors='replace') as f:
                root=ET.parse(f)
            
            for skill in root.iter("Skill"):
            
                obj={}
                obj["ClassName"]=skill.get("Name")
                obj["TargetBuffs"]=[]
                #if obj['ClassName'] == 'Cryomancer_SubzeroShield':
                #    flag = 0
                #    test = skill
                #    break;
                # skill -> resultlist
                for resultlist in skill.iter("ResultList"):
                    for toolscp in resultlist.iter("ToolScp"):
                        scp=toolscp.get("Scp")
                        if scp=="S_R_TGTBUFF":
                            #targetbuff
                            elems=list(toolscp.iter())
                            buff=[
                                #link, duration, chance
                                 elems[1].get("Str"),str(float(elems[4].get("Num"))/1000.0),str(elems[6].get("Num"))
                            ]
                            obj["TargetBuffs"].append(';'.join(buff))
                            
                for etc in skill.iter("EtcList"):
                   
                    for toolscp in etc.iter("Scp"):
                        scp=toolscp.get("Scp")
                        if scp=="SKL_BUFF":
                            #selfbuff
                            elems=list(toolscp.iter())
                            lua = luautil.lua 
                            dur  = str(float(elems[4].get("Num"))/1000.0)
                            if (elems[4].get('UseFunc') ==1):
                                fun = elems[4].get('FuncTxt')
                                dur = str(lua.execute(fun)/1000)
                                
                            chance = str(elems[6].get("Num"))
                            if (elems[6].get('UseFunc') ==1):
                                fun = elems[4].get('FuncTxt')
                                chance = str(lua.execute(fun)/1000)
                            buff=[
                                #link, duration, chance
                                 elems[1].get("Str"),dur,chance
                            ]
                            obj["TargetBuffs"].append(';'.join(buff))
                
                if len(obj['TargetBuffs']) >0:
                    xml_skills[obj['ClassName']] = obj
        except ET.ParseError as e:
            logging.warning("Parse error:"+str(e))
        #if not flag:
        #    break
    c.data['xml_skills'] = xml_skills