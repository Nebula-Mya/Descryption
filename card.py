import sigils

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
        takeDamage(damage) : reduces current life by damage (in progress)
        play(zone) : activates sigils on entering field, resets stats, and updates zone
        die(left_card, right_card) : activates sigils on death and resets stats (in progress)
        sacc() : resets stats and updates ASCII art without activating sigils on being killed
        explain() : prints explanation of stats and sigil for player
        updateASCII() : updates the ASCII art for the card
    '''
    def __init__(self, name = '      ', cost = 0, attack = 0, life = 0, sigil = '', status = 'alive', zone = 0) :
        self.species = name
        self.name = name.ljust(9)[:9]
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
        if name == '      ' :
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
        self.current_attack = self.base_attack
        self.current_life = self.base_life
        self.is_poisoned = False
        self.zone = 0
        self.status = 'alive'
        self.updateASCII()

    def attack(self, front_left_card, front_card, front_right_card, left_card, right_card) :
        # if sigil is;
        ## bifurcate: attacks front_left_card and front_right_card
        if self.sigil == 'bifurcate' :
            if front_left_card != None :
                front_left_card.takeDamage(self.current_attack)
            if front_right_card != None :
                front_right_card.takeDamage(self.current_attack)
        ## lane shift right: attacks front, then moves a lane right if possible
            # if right_card is blank and self.zone isn't 5, move to the right
        elif self.sigil == 'lane shift right' :
            front_card.takeDamage(self.current_attack)
            if (self.zone != 5) and (right_card.name == '      ') :
                self.zone += 1
                right_card.zone -= 1
        ## lane shift left: attacks front, then moves a lane left if possible
            # if left_card is blank and self.zone isn't 1, move to the left
        elif self.sigil == 'lane shift left' :
            front_card.takeDamage(self.current_attack)
            if (self.zone != 1) and (left_card.name == '      ') :
                self.zone -= 1
                left_card.zone += 1
        ## venom: attacks front, then poisons front
        elif self.sigil == 'venom' :
            front_card.takeDamage(self.current_attack)
            front_card.is_poisoned = True
        ## irrelevant or no sigil: attacks front
        else :
            front_card.takeDamage(self.current_attack)
        # if poisoned, deal 1 damage to self
        if self.is_poisoned :
            self.takeDamage(1)

    def __str__(self) :
        print(self.name)
    
    def displayFull(self) :
        print(self.text)

    def TextByLine(self) :
        self.line_cursor += 1
        if self.line_cursor == 13 : 
            self.line_cursor = 2
        return self.text_lines[self.line_cursor - 1]

    def takeDamage(self, damage) :
        if self.name == '      ' or self.status == 'dead':
            # deal damage to opposite player
            pass
        else :
            self.current_life -= damage
            self.updateASCII()
            if self.current_life <= 0 :
                self.status = 'dead'

    def play(self, zone) :
        self.resetStats()
        self.zone = zone
        self.updateASCII()

    def die(self, left_card, right_card) :
        if self.sigil == 'split' :
            self.resetStats()
            self.updateASCII()
            if self.base_life > 1 and self.base_attack > 1 :
                if left_card.name == '     ' and self.zone != 1 :
                    # play a copy of self with halved stats and no sigil to the left
                    pass
                if right_card.name == '     ' and self.zone != 5 :
                    # play a copy of self with halved stats and no sigil to the right
                    pass
        elif self.sigil == 'unkillable' :
            if self.name == 'Ouroboros' :
                self.base_attack += 1
                self.base_life += 1
            self.resetStats()
            self.status = 'undead'
            self.updateASCII()
        else :
            self.resetStats()
            self.updateASCII()
        
    def sacc(self) :
        if self.sigil == 'unkillable' :
            if self.name == 'Ouroboros' :
                self.base_attack += 1
                self.base_life += 1
            self.resetStats()
            self.status = 'undead'
            self.updateASCII()
        else :
            self.resetStats()
            self.updateASCII()

    def explain(self) :
        description = '''
    ,-------------,
    |{species} {C}|         {card} requires {saccs} sacrifices to summon.
    |             |
    |             |
    |    {rw1}    |
    |    {rw2}    |         {sigil} sigil: {desc}
    |    {rw3}    |
    |             |
    |             |
    |          {S}|         {card} has an attack power of {attack} and life points {life} of {max_life}.
    '-------------'
    '''.format(species=self.name, C=self.cost, rw1=sigils.Dict[self.sigil][0][0], rw2=sigils.Dict[self.sigil][0][1], rw3=sigils.Dict[self.sigil][0][2], S=self.stats, saccs=self.saccs, sigil=self.sigil.title(), desc=sigils.Dict[self.sigil][1], attack=self.current_attack, life=self.current_life, max_life=self.base_life, card=self.species)
        print(description)

    def updateASCII(self) :
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