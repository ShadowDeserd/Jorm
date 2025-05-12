
#import skills
import copy
from configuration.config import ItemType, EquipmentSlotType, ITEMS, StatType
import uuid
from items.misc import Item
from items.consumable import Consumable
from items.equipment import Equipment, EquipmentBonus
from items.error import ErrorItem

import random
def load_item(item_premade_id, unique_id = None, max_stats = False): # unique_id is used for equipment seeds

    premade_id = item_premade_id
    if premade_id not in ITEMS:
        new_item = ErrorItem()
        new_item.name = '@yellowERROR@normal'
        new_item.description = 'id: '+str(premade_id)
        new_item.premade_id = premade_id
        return new_item

    item_type = ITEMS[premade_id]['item_type']

    if item_type == ItemType.EQUIPMENT:
        new_item = Equipment()
        new_item.new = True

        
        for key in ITEMS[premade_id]['stats']:
            new_item.stat_manager.stats[key] += ITEMS[premade_id]['stats'][key]

        for key in ITEMS[premade_id]['requirements']:
            new_item.stat_manager.reqs[key] += ITEMS[premade_id]['requirements'][key]
        
        if unique_id == None:
            unique_id = new_item.id

        if ITEMS[premade_id]['bonuses'] != 0:
            for b in ITEMS[premade_id]['bonuses'].split(','):
                _type = b.split(':')[0]
                _key = b.split(':')[1].split('=')[0]
                _val = int(b.split('=')[1])
                val = _val
                boon = EquipmentBonus(  
                                        type = _type, 
                                        key = _key, 
                                        val = val,
                                        premade_bonus = True
                                    )
                new_item.manager.add_bonus(boon)

        '''
        # set unique ID now for the seed
        if unique_id == None:
            unique_id = new_item.id


            for key in ITEMS[premade_id]['stats']:
                #new_item.stat_manager.stats[key] += ITEMS[premade_id]['stats'][key]
                val = ITEMS[premade_id]['stats'][key]
                if val<=0:
                    val = int(random.randint(val,0))
                else:
                    val = int(random.randint(0,val))

                if max_stats:
                    val = ITEMS[premade_id]['stats'][key]

                boon = EquipmentBonus(  
                                        type = 'stat', 
                                        key = key, 
                                        val = val,
                                        premade_bonus = False
                                    )
                new_item.manager.add_bonus(boon)

            # 0 is the placeholder for no skill
            if ITEMS[premade_id]['bonuses'] != 0:
                for b in ITEMS[premade_id]['bonuses'].split(','):
                    _type = b.split(':')[0]
                    _key = b.split(':')[1].split('=')[0]
                    _val = int(b.split('=')[1])
                    #print(b)
                    val = _val
                    if val<=0:
                        val = int(random.randint(val,0))
                    else:
                        val = int(random.randint(0,val))

                    if max_stats:
                        val = _val

                    boon = EquipmentBonus(  
                                            type = _type, 
                                            key = _key, 
                                            val = val,
                                            premade_bonus = False
                                        )
                    new_item.manager.add_bonus(boon)
        '''

            
        '''
        #print(unique_id)
        uuid_str = str(unique_id)  # Example UUID
        uuid_int = int(uuid.UUID(uuid_str))

        rng_seed = int(uuid_int)
        myrandom = random.Random(rng_seed)
        rank = 0
        for i in range(0,myrandom.randrange(new_item.stat_manager.reqs[StatType.LVL])):
            stat_to_affect = myrandom.choice([key for key in new_item.stat_manager.stats])
            boost = myrandom.choice([-1,1,2])
            rank += boost
            if stat_to_affect in [StatType.HPMAX, StatType.MPMAX]:
                boost = boost * 5
            new_item.stat_manager.stats[stat_to_affect] += boost
            if stat_to_affect not in [StatType.ARMOR, StatType.MARMOR]:
                new_item.stat_manager.reqs[stat_to_affect] += abs(boost) 
        new_item.rank = rank
        '''

        new_item.new = False
        new_item.slot = ITEMS[premade_id]['slot']

    if item_type == ItemType.MISC:
        new_item = Item()

    if item_type == ItemType.CONSUMABLE:
        new_item = Consumable()

        
        new_item.skill_manager.skills = ITEMS[premade_id]['skills']
        new_item.use_perspectives = ITEMS[premade_id]['use_perspectives']


    
    new_item.name = ITEMS[premade_id]['name']
    new_item.description = ITEMS[premade_id]['description']
    new_item.premade_id = ITEMS[premade_id]['premade_id']


    # on creation of an item object, it receives a uuid
    # if there is no uuid present in the item dict received, then that item is being created for the first time
    # and if there is uuid present, then the item is most likely loaded from the database and should
    # receive its id, and not get a new randomly generated one
    

    return new_item
  

def save_item(item):
    return item.to_dict()


