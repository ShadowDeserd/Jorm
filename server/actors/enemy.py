from actors.actor import Actor

import actors.enemy_ai as enemy_ai

import random

import copy

from configuration.config import StatType, ItemType, ENEMIES, ITEMS

from items.manager import load_item

from configuration.config import ITEMS

from quest import ObjectiveCountProposal, OBJECTIVE_TYPES

def create_enemy(room, enemy_id, spawn_for_lore = False):
    if enemy_id not in ENEMIES:
        print(f'error creating enemy: {enemy_id}')
        return

    enemy = ENEMIES[enemy_id]
    name = ''
    if not spawn_for_lore:
        names = 'Redpot Kuro Christine Adne Ken Thomas Sandra Erling Viktor Wiktor Sam Dan Arr\'zTh-The\'RchEndrough'
        name = random.choice(names.split())
        name = name + ' The ' + enemy['name']
    else:
        name = enemy['name']
    stats = enemy['stats']
    skills = enemy['skills']
    combat_loop = enemy['combat_loop']
    _loot = enemy['loot']
    loot = _loot
    #print(enemy['name'],LOOT[_loot],'XD')

        

    for item in loot.keys():
        #print(loot)
        if item not in ITEMS:
            print(item, 'does not exist in loot table for ', enemy_id)
    e = Enemy(enemy_id, name, room, stats, loot, skills, combat_loop)
    e.description = enemy['description']

    return e

class Enemy(Actor):
    def __init__(self, enemy_id, name, room, stats, loot, skills, combat_loop):
        super().__init__(name, room)
        self.enemy_id = enemy_id
        self.stats = {**self.stats, **stats}
        
        #self.stats = 
        self.stats[StatType.HPMAX] = self.stats[StatType.HP]
        self.stats[StatType.MPMAX] = self.stats[StatType.MP]

        self.loot = copy.deepcopy(loot)
        self.skills = copy.deepcopy(skills)
        self.combat_loop = copy.deepcopy(combat_loop)

        self.ai = enemy_ai.AIBasic(self)
        self.room.move_entity(self)


    def tick(self):
        self.ai.tick()

    def drop_loot(self,entity):
        all_items = ITEMS
        
        for item in self.loot: 
            roll = random.random()
            if roll >= self.loot[item]:
                continue

            new_item = load_item(item)

            #if new_item.item_type == ItemType.EQUIPMENT:
            #    for i in range(random.randint(0,new_item.requirements[StatType.LVL])):
            #        stat = random.choice([s for s in new_item.stats.keys()])
            #        new_item.stats[stat] = new_item.stats[stat] + 1

            
            if entity.inventory_manager.add_item(new_item):   
                entity.sendLine(f'You loot {new_item.name}')
            else:
                entity.sendLine(f'Your inventory is full and you missed out on {new_item.name}')

    def die(self):
        
        if self.room == None:
            super().die()
            return
        if self.room.combat == None:
            super().die()
            return
        if self not in self.room.combat.participants.values():
            super().die()
            return
        
        for entity in self.room.combat.participants.values():
            if type(entity).__name__ == "Player":
                entity.stats[StatType.EXP] += self.stats[StatType.EXP]
                self.drop_loot(entity)
                proposal = ObjectiveCountProposal(OBJECTIVE_TYPES.KILL_X, self.enemy_id, 1)
                entity.quest_manager.propose_objective_count_addition(proposal)
                
        super().die()


    def set_turn(self):
        super().set_turn()
