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

    Methods :
        resetStats() : sets current stats to base stats
        attack(left_card, front_card, right_card) : attacks zone(s) in front
        print() : prints self.name
        displayFull() : prints full card
        displayByLine() : prints one line for each call
        takeDamage(damage) : reduces current life by damage
        play(zone) : plays card onto field
        die(zone) : replaces self with BlankCard
        explain() : prints explanation of stats and sigil for player

    '''
    def __init__(self, name = '      ', cost = ' ', attack = ' ', life = ' ', sigil = '', sigil_text = ['     ','     ','     ']) :
        self.name = name
        self.cost = str("C:" + cost)
        self.base_attack = attack
        self.current_attack = attack
        self.base_life = life
        self.life = life
        self.sigil = sigil
        self.sigil_icon = sigil_text
        self.stats = str(self.current_attack + "/" + self.life)
        if name == '      ' :
            self.cost = '   '
            self.stats = '   '
        self.text = '''
,-------------,
|{name}    {C}|
|             |
|             |
|    {rw1}    |
|    {rw2}    |
|    {rw3}    |
|             |
|             |
|          {S}|
'-------------'
'''.format(name = self.name, C = self.cost, rw1 = self.sigil_icon[0], rw2 = self.sigil_icon[1], rw3 = self.sigil_icon[2], S = self.stats)
        self.text_lines = self.text.split("\n")
        self.line_cursor = 0
        
    def resetStats(self) :
        pass

    def attack(self, left_card, front_card, right_card) :
        pass

    def __str__(self) :
        print(self.name)
    
    def displayFull(self) :
        print(self.text)

    def displayByLine(self) :
        print(self.text_lines[self.line_cursor], end = '')
        self.line_cursor += 1
        if self.line_cursor == 11 : 
            self.line_cursor = 0

    def takeDamage(self, damage) :
        pass

    def play(self, zone) :
        pass

    def die(self, zone) :
        pass

    def explain(self) :
        pass

if __name__ == "__main__" :
    testblank = BlankCard()
    testblank.displayFull()
    print(str(len(testblank.text_lines)))