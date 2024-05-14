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
        super().__init__(name='Dumpy Tree Frog', cost=1, attack=2, life=2)

class Turtle(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Turtle', cost=1, attack=0, life=4)

class Asp(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Asp', cost=2, attack=2, life=1, sigil='venom')

class Falcon(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Falcon', cost=2, attack=3, life=1, sigil='airborne')

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

class Cockroach(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Cockroach', cost=2, attack=1, life=1, sigil='unkillable')

class Stoat(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Stoat', cost=1, attack=1, life=3)

class Wolf(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Wolf', cost=2, attack=3, life=2)

class Grizzly(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Grizzly', cost=3, attack=4, life=6)

class Urayuli(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Urayuli', cost=4, attack=7, life=7)

class Raven(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Raven', cost=2, attack=2, life=3, sigil='airborne')

class Bee(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Bee', cost=0, attack=1, life=1, sigil='airborne')

class Bullfrog(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Bullfrog', cost=1, attack=1, life=2, sigil='mighty leap')

class BlackGoat(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Black Goat', cost=0, attack=1, life=0, sigil='worthy sacrifice')

class Beehive(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Beehive', cost=1, attack=0, life=2, sigil='bees within')

class Cat(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Cat', cost=1, attack=0, life=1, sigil='many lives')
        self.spent_lives = 0

class UndeadCat(card.BlankCard) :
    def __init__(self) :
        super().__init__(name='Undead Cat', cost=1, attack=3, life=6)

# Allowed cards:
Poss_Playr = {
    0 : [Rabbit(), Shrew(), BlackGoat()],
    1 : [DumpyTF(), Turtle(), Stoat(), Bullfrog(), Beehive()],
    2 : [Asp(), Falcon(), Cockroach(), Wolf(), Raven()]*3 + [Ouroboros()],
    3 : [Lobster(), Grizzly()],
    4 : [BoppitW(), Urayuli()]
}
Poss_Leshy = {
    0 : [OppositeRabbit(), OppositeShrew(), Squirrel()],
    1 : [DumpyTF(), Turtle(), Stoat(), Bullfrog()],
    2 : [Asp(), Falcon(), Cockroach(), Wolf(), Raven()]
}