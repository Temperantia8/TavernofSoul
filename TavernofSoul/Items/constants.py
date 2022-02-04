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
