import sigils
import os

class BlankCard() :
    '''
    An empty card, serves both as an empty zone and as the parent class for all other cards

    Arguments :
        name : the name of the card (str)
        cost : number of sacrifices needed for summoning (int)
        attack : base attack stat (int)
        life : base life stat (int)
        sigil : the sigil the card currently has (str)
        status : whether the card is alive or dead (str)
        zone : the zone the card is in, with 0 as default (int)
    
    Other Attributes :
        species : the name of the card without truncating or padding (str)
        is_poisoned : whether the card is poisoned (bool)
        saccs : the cost without formatting (int)
        base_attack : the base attack stat (int)
        current_attack : the current attack stat (int)
        base_life : the base life stat (int)
        current_life : the current life stat (int)
        text : the ASCII art for the card (str)
        text_lines : the ASCII art for the card split by line (list)
        line_cursor : the current line to print (int)

    Methods :
        resetStats() : sets current stats to base stats
        attack(front_left_card, front_card, front_right_card, left_card, right_card) : attacks zone(s) in front
        print() : prints self.name
        displayFull() : prints full card
        displayByLine() : prints one line for each call
        takeDamage(damage) : reduces current life by damage 
        play(zone) : activates sigils on entering field, resets stats, and updates zone
        die(left_card, right_card, field) : activates sigils on death and resets stats
        sacc() : resets stats and updates ASCII art without activating sigils on being killed
        explain() : prints explanation of stats and sigil for player
        updateASCII() : updates the ASCII art for the card
    '''
    def __init__(self, name = '', cost = 0, attack = 0, life = 0, sigil = '', status = 'alive', zone = 0) :
        self.species = name
        self.name = name.ljust(9)[:9]
        if len(self.name) < len(name) and self.name[-2:] != '  ' :
            self.name = self.name[:-1] + '.'
        self.saccs = cost
        self.cost = str("C:" + str(cost))
        self.base_attack = attack
        self.current_attack = attack
        self.base_life = life
        self.current_life = life
        self.sigil = sigil
        self.is_poisoned = False
        self.status = status
        self.zone = zone
        if self.species == '' :
            self.cost = '   '
            self.stats = '   '
        else :
            self.stats = hex(self.current_attack % 16)[2] + "/" + hex(self.current_life % 16)[2]
        self.text = '''
,-------------,
|{species} {C}|
|             |
|             |
|    {rw1}    |
|    {rw2}    |
|    {rw3}    |
|             |
|             |
|          {S}|
'-------------'
'''.format(species = self.name, C = self.cost, rw1 = sigils.Dict[self.sigil][0][0], rw2 = sigils.Dict[self.sigil][0][1], rw3 = sigils.Dict[self.sigil][0][2], S = self.stats)
        self.text_lines = self.text.split("\n")
        self.line_cursor = 1
        
    def resetStats(self) :
        '''
        resets current stats to base stats
        '''
        self.current_attack = self.base_attack
        self.current_life = self.base_life
        self.is_poisoned = False
        self.zone = 0
        self.status = 'alive'
        self.updateASCII()

    def attack(self, front_left_card, front_card, front_right_card, left_card, right_card) :
        '''
        attacks zone(s) in front

        Arguments:
            front_left_card: the card in the zone to the left of the front card (card object)
            front_card: the card in the zone in front of the attacking card (card object)
            front_right_card: the card in the zone to the right of the front card (card object)
            left_card: the card in the zone to the left of the attacking card (card object)
            right_card: the card in the zone to the right of the attacking card (card object)
        
        Returns:
            opponent_teeth: the damage dealt to the opponent (int)
            controller_teeth: the damage dealt to the controller (int)
        '''
        opponent_teeth = 0
        controller_teeth = 0
        # if sigil is;
        ## bifurcate: attacks front_left_card and front_right_card
        if self.sigil == 'bifurcate' :
            if front_left_card != None :
                opponent_teeth += front_left_card.takeDamage(self.current_attack)
            if front_right_card != None :
                opponent_teeth += front_right_card.takeDamage(self.current_attack)
        ## venom: attacks front, then poisons front
        elif self.sigil == 'venom' :
            opponent_teeth += front_card.takeDamage(self.current_attack)
            front_card.is_poisoned = True
        ## irrelevant or no sigil: attacks front
        else :
            opponent_teeth += front_card.takeDamage(self.current_attack)
        # if poisoned, deal 1 damage to self
        if self.is_poisoned :
            controller_teeth += self.takeDamage(1)
        return (opponent_teeth, controller_teeth)

    def __str__(self) :
        print(self.name)
    
    def displayFull(self) :
        '''
        prints full card ASCII art
        '''
        print(self.text)

    def TextByLine(self) :
        '''
        returns one line of the card's ASCII art at a time
        '''
        self.line_cursor += 1
        if self.line_cursor == 13 : 
            self.line_cursor = 2
        return self.text_lines[self.line_cursor - 1]

    def takeDamage(self, damage) :
        '''
        reduces current life by damage

        Arguments:
            damage: the amount of damage to take (int)

        Returns:
            teeth: damage to controller (int)
        '''
        if self.species == '' :
            teeth = damage
        elif self.status == 'dead' :
            teeth = damage
        else :
            self.current_life -= damage
            teeth = 0
            self.updateASCII()
            if self.current_life <= 0 :
                self.status = 'dead'
                teeth = abs(self.current_life)
        return teeth

    def play(self, zone) :
        '''
        activates sigils on entering field, resets stats, and updates zone
        '''
        self.resetStats()
        self.zone = zone
        self.updateASCII()

    def die(self, left_card, right_card, field) :
        '''
        activates sigils on death and resets stats

        Arguments:
            left_card: the card in the zone to the left of the dying card (card object)
            right_card: the card in the zone to the right of the dying card (card object)
            field: the dict of the controller's field (dict)
        '''
        if self.name == 'Ouroboros' :
            self.base_attack += 1
            self.base_life += 1
            new_stats = '''{a}
{l}'''.format(a=self.base_attack,l=self.base_life)
            import sys
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                data_file = 'Descryption_Data/data.txt'
            else:
                data_file = 'data.txt'
            with open(data_file, 'w') as file :
                file.write(new_stats)
        self.resetStats()
        self.updateASCII()
        
    def sacc(self) :
        '''
        resets stats and updates ASCII art without activating sigils on being killed, only on any death
        '''
        if self.name == 'Ouroboros' :
                self.base_attack += 1
                self.base_life += 1
                new_stats = '''{a}
{l}'''.format(a=self.base_attack,l=self.base_life)
                import sys
                if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                    data_file = 'Descryption_Data/data.txt'
                else:
                    data_file = 'data.txt'
                with open(data_file, 'w') as file :
                    file.write(new_stats)
        self.resetStats()
        self.updateASCII()

    def explain(self) :
        '''
        prints explanation of stats and sigil for player
        '''
        (term_cols, term_rows) = os.get_terminal_size()
        card_gaps = (term_cols*55 // 100) // 5 - 15
        if self.sigil.title() == '' :
            sigil_text = 'No'
        else :
            sigil_text = self.sigil.title()
        description = """{spc},-------------,
{spc}|{species} {C}|  {spc}{card} requires {saccs} sacrifices to summon.
{spc}|             |
{spc}|             |
{spc}|    {rw1}    |
{spc}|    {rw2}    |  {spc}{sigil} sigil: {desc}
{spc}|    {rw3}    |
{spc}|             |
{spc}|             |
{spc}|          {S}|  {spc}{card} has an attack power of {attack} and life points {life} of {max_life}.
{spc}'-------------'""".format(species=self.name, C=self.cost, rw1=sigils.Dict[self.sigil][0][0], rw2=sigils.Dict[self.sigil][0][1], rw3=sigils.Dict[self.sigil][0][2], S=self.stats, saccs=self.saccs, sigil=sigil_text, desc=sigils.Dict[self.sigil][1], attack=self.current_attack, life=self.current_life, max_life=self.base_life, card=self.species, spc=' '*card_gaps)
        print(description)

    def updateASCII(self) :
        '''
        updates the ASCII art for the card
        '''
        if self.species == '' :
            self.cost = '   '
            self.stats = '   '
        else :
            self.stats = hex(self.current_attack % 16)[2] + "/" + hex(self.current_life % 16)[2]
        self.text = '''
,-------------,
|{species} {C}|
|             |
|             |
|    {rw1}    |
|    {rw2}    |
|    {rw3}    |
|             |
|             |
|          {S}|
'-------------'
    '''.format(species=self.name, C=self.cost, rw1=sigils.Dict[self.sigil][0][0], rw2=sigils.Dict[self.sigil][0][1], rw3=sigils.Dict[self.sigil][0][2], S=self.stats)
        self.text_lines = self.text.split("\n")
        self.line_cursor = 1

if __name__ == "__main__" :
    testblank = BlankCard()
    testsigil = slot4 = BlankCard(name='test',cost=3,attack=1,life=2,sigil='bifurcate')
    print()
    print('Blank Card')
    testblank.displayFull()
    # print(str(len(testblank.text_lines)))
    # print(testblank.text_lines)
    print()
    print('Sigil Card')
    testsigil.takeDamage(1)
    testsigil.explain()
    # print(str(len(testsigil.text_lines)))
    # print(testsigil.text_lines)