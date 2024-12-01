from config import DamageType, StatType

class Affect:
    def __init__(self, _id, affect_manager, name, description, turns):
        self.id = _id
        self.affect_manager = affect_manager
        self.owner = self.affect_manager.owner
        self.name = name
        self.description = description
        self.turns = turns

    def info(self):
        return f'{self.name:<15} {self.turns:<3} {self.description}\n'

    # called when applied 
    def on_applied(self):
        self.affect_manager.owner.simple_broadcast(
            f'You are {self.name}',
            f'{self.affect_manager.owner.pretty_name()} is {self.name}',
        )

    # called when effect is over
    def on_finished(self, silent = False):
        if not silent:
            self.affect_manager.owner.simple_broadcast(
                f'You are no longer {self.name}',
                f'{self.affect_manager.owner.pretty_name()} is no longer {self.name}\n',
            )
        self.affect_manager.pop_affect(self)

    # called at start of turn
    def set_turn(self):
        pass

    # called at end of turn
    def finish_turn(self):
        self.turns -= 1

    # called whenever hp updates in any way
    def take_damage(self, source, damage, damage_type):
        return source, damage, damage_type

class AffectStunned(Affect):
    # called at start of turn
    def set_turn(self):
        self.owner.simple_broadcast(
            f'You are too stunned to act!',
            f'{self.owner.pretty_name()} is too stunned to act!')
        self.owner.finish_turn()

class AffectEthereal(Affect):
    def __init__(self, _id, affect_manager, name, description, turns, dmg_amp):
        super().__init__(_id, affect_manager, name, description, turns)
        self.dmg_amp = dmg_amp
    
    def take_damage(self, source, damage, damage_type):

        if damage_type == DamageType.PHYSICAL:
            damage_type = DamageType.CANCELLED
            self.owner.sendLine(
                'The attack goes straight thru you as you are ethereal!',
                f'The attack goes straight thru {self.owner.pretty_name()} as they are ethereal!')

        if damage_type == DamageType.MAGICAL:
            damage = int(damage * self.dmg_amp)

        return source, damage, damage_type