import sigils
import os
import QoL

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
        blank_cost : whether the card has a blank cost (bool)
        blank_stats : whether the card has blank stats (bool)
    
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
    def __init__(self, name = '', cost = 0, attack = 0, life = 0, sigil = '', status = 'alive', zone = 0, blank_cost = False, blank_stats = False) :
        self.species = name
        if name == '' or blank_cost : # takes advantage of extra space from having no cost
            self.name = name.ljust(12)[:12]
        else :
            self.name = name.ljust(9)[:9]
        if len(self.name) < len(name) and self.name[-2:] != '  ' :
            self.name = self.name[:-1] + '.'
        self.saccs = cost
        self.base_attack = attack
        self.current_attack = attack
        self.base_life = life
        self.current_life = life
        self.sigil = sigil
        self.is_poisoned = False
        self.status = status
        self.zone = zone
        self.blank_cost = blank_cost
        self.blank_stats = blank_stats
        if self.blank_cost or self.species == '':
            self.cost = ''
        else :
            self.cost = str("C:" + str(cost))
        if self.blank_stats or self.species == '':
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
        if self.species == 'Cat' :
            self.spent_lives = 0
        self.updateASCII()

    def attack(self, front_left_card, front_card, front_right_card, is_players=False, bushes={}) :
        '''
        attacks zone(s) in front

        Arguments:
            front_left_card: the card in the zone to the left of the front card (card object)
            front_card: the card in the zone in front of the attacking card (card object)
            front_right_card: the card in the zone to the right of the front card (card object)
            is_players: whether the attacking card is on the player's field (bool)
            bushes: the dict of bushed cards (dict)
        
        Returns:
            points: the damage dealt to the opponent (int)
        '''
        ### future code
        # setup variables
        if is_players :
            to_opp_field = True
        else :
            to_opp_field = False
        points = 0

        # if sigil is a sigil that activates on attack, execute the code
        if self.sigil in sigils.on_attacks :
            local_dict = locals()
            exec(sigils.Dict[self.sigil][2], None, local_dict)
            points = local_dict['points']

        # if sigil is irrelevant or none existent, attack front
        else :
            points += front_card.takeDamage(self.current_attack, in_opp_field=to_opp_field, bushes=bushes)
        
        # if poisoned, deal 1 damage to self
        if self.is_poisoned :
            self.takeDamage(1)

        return points

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

    def takeDamage(self, damage, from_air=False, in_opp_field=False, in_bushes=False, bushes={}, deathtouch=False) :
        '''
        reduces current life by damage

        Arguments:
            damage: the amount of damage to take (int)
            from_air: whether the damage is from an airborne creature (bool)
            in_opp_field: whether the card is on Leshy's feild (bool)
            in_bushes: whether the card is in the bushes (bool)
            bushes: the dict of bushed cards (dict)

        Returns:
            teeth: damage to controller (int)
        '''
        teeth = 0
        if (self.species == '' or self.status == 'dead' or (from_air and self.sigil != 'mighty leap') or self.sigil == 'waterborne') and not in_bushes :
            teeth = damage
        else :
            prev_life = self.current_life
            self.current_life -= damage
            self.updateASCII()
            if self.current_life <= 0 or deathtouch:
                self.status = 'dead'
                if in_opp_field and self.current_life <= 0 :
                    excess_damage = damage - prev_life
                    bushes[self.zone].takeDamage(excess_damage, from_air, in_bushes=True)
        return teeth

    def play(self, zone) :
        '''
        activates sigils on entering field, resets stats, and updates zone
        '''
        self.resetStats()
        self.zone = zone
        self.updateASCII()

    def die(self) :
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
            QoL.write_file('data.txt', 'Descryption_Data/data.txt', [str(self.base_attack), str(self.base_life)])
        self.resetStats()
        self.updateASCII()
        
    def sacc(self) :
        '''
        resets stats and updates ASCII art without activating sigils on being killed, only on any death
        '''
        if self.species == 'Cat' :
            self.spent_lives += 1
        elif self.species == 'Ouroboros' :
            self.base_attack += 1
            self.base_life += 1
            QoL.write_file('data.txt', 'Descryption_Data/data.txt', [str(self.base_attack), str(self.base_life)])
            self.resetStats()
            self.updateASCII()
        else :
            self.resetStats()
            self.updateASCII()

    def explain(self) :
        '''
        prints explanation of stats and sigil for player
        '''
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15
        if self.sigil.title() == '' :
            sigil_text = 'No Sigil'
        elif 'hefty' in self.sigil:
            sigil_text = 'Hefty:'
        else :
            sigil_text = QoL.title_case(self.sigil) + ':'
        # get parameters for sigil description
        max_desc_first = term_cols - 18 - card_gaps*2 - len(sigil_text)
        max_desc_rest = term_cols - 14 - card_gaps*2
        # split description into lines
        [desc_first_line, desc_second_line, desc_third_line] = QoL.split_nicely(sigils.Dict[self.sigil][1], max_desc_first, max_desc_rest, max_lines=3, add_blank_lines=True)

        description = """{spc},-------------,
{spc}|{species} {C}|  {spc}{card} requires {saccs} sacrifices to summon.
{spc}|             |
{spc}|             |
{spc}|    {rw1}    |
{spc}|    {rw2}    |  {spc}{sigil} {desc1}
{spc}|    {rw3}    |      {spc}{desc2}
{spc}|             |      {spc}{desc3}
{spc}|             |
{spc}|          {S}|  {spc}{card} has an attack power of {attack} and life points {life} of {max_life}.
{spc}'-------------'""".format(species=self.name, C=self.cost, rw1=sigils.Dict[self.sigil][0][0], rw2=sigils.Dict[self.sigil][0][1], rw3=sigils.Dict[self.sigil][0][2], S=self.stats, saccs=self.saccs, sigil=sigil_text, attack=self.current_attack, life=self.current_life, max_life=self.base_life, card=self.species, spc=' '*card_gaps, desc1=desc_first_line, desc2=desc_second_line, desc3=desc_third_line)
        print(description)

    def updateASCII(self) :
        '''
        updates the ASCII art for the card
        '''
        if self.blank_cost or self.species == '':
            self.cost = ''
        else :
            self.cost = str("C:" + str(self.saccs))
        if self.blank_stats or self.species == '':
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