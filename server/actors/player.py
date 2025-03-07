from actors.actor import Actor
import utils
from trade import TradeManager
# import commands maps
from actors.player_only_functions.commands import one_letter_commands, commands
# import the commands module so all functions can be imported and assigned to player class
import actors.player_only_functions.commands 

import time



class Player(Actor):
    def __init__(self, protocol, name, room, _id = None):
        self.protocol = protocol
        
        super().__init__(name, room, _id)

        self.last_line_sent = None
        self.last_command_used = None

        self.admin = 0
        self.check_if_admin()

        self.recall_site = 'tutorial'
        self.trade_manager = TradeManager(self)

        if self.room != None:
            self.room.move_entity(self, silent = True)

        # meta data
        self.date_of_creation = utils.get_unix_timestamp()
        self.date_of_last_login = utils.get_unix_timestamp()
        self.time_in_game = 0
        

    def check_if_admin(self):
        if self.protocol == None:
            return
        
        admins = self.protocol.factory.db.read_admins(self)
        
        if admins == None:
            self.admin = 0
        else:
            self.admin = admins[1]
        
    def set_admin(self, admin_level):
        self.admin = admin_level

    def get_character_sheet(self):
        output = super().get_character_sheet()
        return output

    def sendLine(self, line, color = True):
        if color:
            line = utils.add_color(f'{line}\n')
            # send null byte several times to indicate new line
            self.protocol.transport.write(b'\x00\x00\x00\x00\x00' + line.encode('utf-8'))
        else:
            self.protocol.transport.write(b'\x00\x00\x00\x00\x00' + line.encode('utf-8'))
        return

    def handle(self, line):
        # empty lines are handled as resend last line

        if self.current_dialog != None:
            self.current_dialog.answer(line)
            return
            
        
        if not line: 
            line = self.last_line_sent
            if not line:
                return

        self.last_line_sent = line

        command = line.split()[0]
        line = " ".join(line.split()[1::]).strip()

        if command in one_letter_commands:
            script = getattr(self, commands[one_letter_commands[command]])
            self.last_command_used = one_letter_commands[command]
            script(line)
            return
        
        best_match, best_score = utils.match_word(command, commands.keys(), get_score = True)
        if best_score < 75:
            self.sendLine(f'You wrote "{command}" did you mean "{best_match}"?\nUse "help {best_match}" to learn more about this command.')
            return

        
        script = getattr(self, commands[best_match])
        self.last_command_used = best_match
        script(line)

# Compile all player functions
# grabs all imported functions inside of actors.player_only_functions 
# and adds those functions to the player object 
for func_name in dir(actors.player_only_functions.commands):
    func = getattr(actors.player_only_functions.commands, func_name)
    # Only assign functions to the Player class
    if callable(func):
        setattr(Player, func_name, func)
            
            