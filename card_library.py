import card

class Squirrel(card.BlankCard) :
    '''
    A squirrel card, which can be used as a resource to play other cards.
    '''
    def __init__(self) :
        super().__init__(name='Squirrel', cost=0, attack=0, life=1)

class Rabbit(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Rabbit', cost=0, attack=1, life=1, sigil='lane shift right')
    
class OppositeRabbit(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Rabbit', cost=0, attack=1, life=1, sigil='lane shift left')

class Shrew(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Shrew', cost=0, attack=1, life=1, sigil='lane shift left')

class OppositeShrew(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Shrew', cost=0, attack=1, life=1, sigil='lane shift right')

class DumpyTF(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Dumpy Tree Frog', cost=1, attack=1, life=2)

class Turtle(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Turtle', cost=1, attack=0, life=3)

class Asp(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Asp', cost=2, attack=2, life=1, sigil='venom')

class Falcon(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Falcon', cost=2, attack=2, life=2)

class Lobster(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Lobster', cost=3, attack=2, life=3, sigil='bifurcate')

class BoppitW(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Boppit Worm', cost=4, attack=3, life=5, sigil='split')

class Ouroboros(card.BlankCard) :
    def __init__(self) :
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            data_file = 'Descryption_Data/data.txt'
        else:
            data_file = 'data.txt'
        with open(data_file, 'r') as file: 
            [Oro_attack,Oro_life] = file.read().split('\n')
        super().__init__(name='Ouroboros', cost=2, attack=int(Oro_attack), life=int(Oro_life), sigil='unkillable')

# Allowed cards:
Poss_Playr = {
    0 : [Rabbit(), Shrew()],
    1 : [DumpyTF(), Turtle()],
    2 : [Asp(), Falcon()]*4 + [Ouroboros()],
    3 : [Lobster()],
    4 : [BoppitW()]
}
Poss_Leshy = {
    0 : [OppositeRabbit(), OppositeShrew()],
    1 : [DumpyTF(), Turtle()],
    2 : [Asp(), Falcon()]
}