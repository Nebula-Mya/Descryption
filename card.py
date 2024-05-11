import sigils

class BlankCard() :
    '''
    An empty card, serves both as an empty zone and as the parent class for all other cards

    Attributes :
        name : the name of the card (str)
        cost : number of sacrifices needed for summoning (int)
        attack : base attack stat (int)
        life : base life stat (int)
        sigil : the sigil the card currently has (str)
        sigil_text : the three lines of ASCII art for the sigil's symbol (str)
        is_poisoned : whether the card is poisoned (bool)
        status : whether the card is alive or dead (str)
        zone : the zone the card is in, with 0 as default (int)

    Methods :
        resetStats() : sets current stats to base stats
        attack(front_left_card, front_card, front_right_card, left_card, right_card) : attacks zone(s) in front
        print() : prints self.name
        displayFull() : prints full card
        displayByLine() : prints one line for each call
        takeDamage(damage) : reduces current life by damage (in progress)
        play(zone) : activates sigils on entering field, resets stats, and updates zone
        die(zone, left_card, right_card) : activates sigils on death and resets stats (in progress)
        explain() : prints explanation of stats and sigil for player (unimplemented)
        updateASCII() : updates the ASCII art for the card
    '''
    def __init__(self, name = '      ', cost = 0, attack = 0, life = 0, sigil = '', sigil_text = ['     ','     ','     '], status = 'alive', zone = 0) :
        self.name = name.ljust(9)[:9]
        self.cost = str("C:" + str(cost))
        self.base_attack = attack
        self.current_attack = attack
        self.base_life = life
        self.current_life = life
        self.sigil = sigil
        self.sigil_icon = sigil_text
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
'''.format(species = self.name, C = self.cost, rw1 = self.sigil_icon[0], rw2 = self.sigil_icon[1], rw3 = self.sigil_icon[2], S = self.stats)
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
        ## blank: attack front_card
        if self.sigil == '' :
            front_card.takeDamage(self.current_attack)
        ## bifurcate: attacks front_left_card and front_right_card
        elif self.sigil == 'bifurcate' :
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
        if self.sigil == '' :
            self.resetStats()
            self.zone = zone
            self.updateASCII()

    def die(self, zone, left_card, right_card) :
        if self.sigil == '' :
            self.resetStats()
            self.updateASCII()
        elif self.sigil == 'split' :
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

    def explain(self) :
        pass

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
    '''.format(species=self.name, C=self.cost, rw1=self.sigil_icon[0], rw2=self.sigil_icon[1], rw3=self.sigil_icon[2], S=self.stats)
        self.text_lines = self.text.split("\n")
        self.line_cursor = 1

if __name__ == "__main__" :
    testblank = BlankCard()
    testsigil = slot4 = BlankCard(name='test',cost=3,attack=1,life=2,sigil='bifurcate',sigil_text=['_   _',' \ / ','  |  '])
    print()
    print('Blank Card')
    testblank.displayFull()
    print(str(len(testblank.text_lines)))
    print(testblank.text_lines)
    print()
    print('Sigil Card')
    testsigil.displayFull()
    print(str(len(testsigil.text_lines)))
    print(testsigil.text_lines)