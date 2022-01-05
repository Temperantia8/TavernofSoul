from Items.constants import bonus_stat_translator, goddess_anvil, goddess_scale, goddess_gabija, goddess_chance, getGoddess

from Items.models import Items, Equipment_Bonus, Item_Recipe_Material
from Items.models import Item_Collection_Material, Item_Collection_Bonus
from Items.models import Goddess_Reinforce_Mat, Goddess_Reinforce_Chance,Eq_Reinf, Eq_TC

def getAnvil(item):

    if item.grade <6: 
        eq_reinf = Eq_Reinf.objects.filter(equipment = item.equipments).order_by('anvil')
        reinf = []
        reinf_price = []
        for anvil in eq_reinf:
            reinf.append(anvil.addatk)
            reinf_price.append(anvil.price)

        eq_tc = Eq_TC.objects.filter(equipment = item.equipments).order_by('tc')
        tc_cost = []
        for tc in eq_tc:
            tc_cost.append(tc.price)
        return reinf, reinf_price, tc_cost

    else:
        lv = item.equipments.level
        tipe = item.equipments.type_equipment.lower()
        
        acc = ['neck', 'ring']
        if tipe in acc:
            tipe = 'acc'
        else:
            tipe = 'armor'
            

        mat = {i : {} for i in range(1,31)}
        for i in Goddess_Reinforce_Mat.objects.filter(lv = lv, eq_type__icontains=tipe).order_by("anvil"):
            mat[ i.anvil][i.mat.ids] = {
                                           'mat_icon' : i.mat.icon,
                                           'mat_name' : i.mat.name,
                                           'mat_ids'  : i.mat.ids,
                                           'mat_count' : i.mat_count
                                       }
                    
        eq_tc = Eq_TC.objects.filter(equipment = item.equipments).order_by('tc')
        tc_cost = []
        for tc in eq_tc:
            tc_cost.append(tc.price)
        
        reinf = { i.anvil :
            {'addatk' : i.addatk, 'addacc': i.addacc, 'chance': i.chance} 
            for i in 
                Goddess_Reinforce_Chance.objects.filter(lv = lv).order_by("anvil")}
        return mat,reinf , tc_cost