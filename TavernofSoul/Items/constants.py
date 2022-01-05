from Items.models import Goddess_Reinforce_Mat, Goddess_Reinforce_Chance
goddess_anvil     = [219,219,219,219,219,
                                     238,238,238,238,238,
                                     256,256,256,256,256,
                                     275,275,275,275,275,
                                     294,294,294,294,294,
                                     294,294,294,294,294,]
goddess_scale     = [3,3,3,3,3,
                     5,5,5,5,5,
                     7,7,7,7,7,
                     8,8,8,8,8,
                     10,11,12,13,14,
                     15,16,17,18,19                    
                     ]
goddess_gabija    = [263,263,263,263,450,
                     450,450,450,450,673,
                     673,673,673,673,927,
                     927,1212,1523,1861,2224,
                     2586,2948,3311,3673,4036,
                     4398,4760,5123,5485,5848]

goddess_chance      = [100,100,100,100,100,
                                          80, 72, 64, 58, 52,
                                          42, 33, 27, 21, 18,
                                          12,  8,  6,  4,  3, 
                                           2, 1,  1,  1,  1 ,
                                           1, 1,  1,  1,  1]

bonus_stat_translator={
    'ADD_CLOTH'     : 'Attack against Cloth Armored Targets',
    'ADD_LEATHER'   : 'Attack against Leather Armored Targets',
    'ADD_CHAIN'     : 'Attack against Chain Armored Targets',
    'ADD_IRON'      : 'Attack against Plate Armored Targets',
    'ADD_GHOST'     : 'Attack against Ghost Armored Targets',
    'ADD_SMALLSIZE' : 'Attack against Small-sized Targets',
    'ADD_MIDDLESIZE': 'Attack against Medium-sized Targets',
    'ADD_LARGESIZE' : 'Attack against Large-sized Targets',
    'ADD_FORESTER'  : 'Attack against Plant-type Targets',
    'ADD_WIDLING'   : 'Attack against Beast-type Targets',
    'ADD_VELIAS'    : 'Attack against Devil-type Targets',
    'ADD_PARAMUNE'  : 'Attack against Mutant-type Targets',
    'ADD_KLAIDA'    : 'Attack against Insect-type Targets',
    'Aries'         : 'Piercing',
    'AriesDEF'      : 'Piercing Defense',
    'SlashDEF'      : 'Slash Defense',
    'StrikeDEF'     : 'Strike Defense',
    'ADD_FIRE'      : 'Add. Fire Property Damage',
    'ADD_ICE'       : 'Add. Ice Property Damage',
    'ADD_POISON'    : 'Add. Poison Property Damage',
    'ADD_LIGHTNING' : 'Add. Lightning Property Damage',
    'ADD_SOUL'      : 'Add. Soul Property Damage',
    'ADD_EARTH'     : 'Add. Earth Property Damage',
    'ADD_HOLY'      : 'Add. Holy Property Damage',
    'ADD_DARK'      : 'Add. Dark Property Damage',
    'RES_FIRE'      : 'Fire Property Resistance',
    'RES_ICE'       : 'Ice Property Resistance',
    'RES_POISON'    : 'Poison Property Resistance',
    'RES_LIGHTNING' : 'Lightning Property Resistance',
    'RES_SOUL'      : 'Soul Property Resistance',
    'RES_EARTH'     : 'Earth Property Resistance',
    'RES_HOLY'      : 'Holy Property Resistance',
    'RES_DARK'      : 'Dark Property Resistance',
    'LootingChance' : 'Looting Chance',
    'UNKNOWN'       : '-'
}

def getGoddess(item):
    """
    

    Parameters
    ----------
    item : TYPE
        DESCRIPTION.

    Returns
    -------
    mat : Dict
        {1: 
           {'00000002': {'mat_icon': 'icon_item_gabijacertificatecoin_1p',
            'mat_name': 'Gabija Coin',
            'mat_ids': '00000002',
            'mat_count': 263},
           '0911030136': {'mat_icon': 'icon_item_misc_vasilisa_notrade',
            'mat_name': '정제된 바실리사의 비늘',
            'mat_ids': '0911030136',
            'mat_count': 3}},
        2: 
           {'0911030136': {'mat_icon': 'icon_item_misc_vasilisa_notrade',
            'mat_name': '정제된 바실리사의 비늘',
            'mat_ids': '0911030136',
            'mat_count': 3},
           '00000002': {'mat_icon': 'icon_item_gabijacertificatecoin_1p',
            'mat_name': 'Gabija Coin',
            'mat_ids': '00000002',
            'mat_count': 263}},
         ...
        }
            
    reinf : Dict
        {1: {'addatk': 219, 'addacc': 0, 'chance': 1.0},
         2: {'addatk': 219, 'addacc': 0, 'chance': 1.0},
         ...
        })

    """
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
                
    
    
    reinf = { i.anvil :
        {'addatk' : i.addatk, 'addacc': i.addacc, 'chance': i.chance} 
        for i in 
            Goddess_Reinforce_Chance.objects.filter(lv = lv).order_by("anvil")}
    
    return mat, reinf
    
    
    
    
    
    
    
    