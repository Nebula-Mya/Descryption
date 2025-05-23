import card
import QoL
import random

class Squirrel(card.BlankCard) :
    '''
    A squirrel card, which can be used as a resource to play other cards.
    '''
    def __init__(self, blank_cost=False) :
        super().__init__(species='Squirrel', cost=0, attack=0, life=1, blank_cost=blank_cost)

class Rabbit(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=['lane shift right',''], blank_cost=blank_cost)
    
class OppositeRabbit(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=['lane shift left',''], blank_cost=blank_cost)

class Shrew(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=['lane shift left',''], blank_cost=blank_cost)

class OppositeShrew(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=['lane shift right',''], blank_cost=blank_cost)

class DumpyTF(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Dumpy Tree Frog', cost=1, attack=2, life=2, blank_cost=blank_cost)

class Turtle(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Turtle', cost=1, attack=0, life=4, blank_cost=blank_cost)

class Asp(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Asp', cost=2, attack=2, life=2, sigils=['venom',''], blank_cost=blank_cost)

class Falcon(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Falcon', cost=2, attack=3, life=1, sigils=['airborne',''], blank_cost=blank_cost)

class Lobster(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Lobster', cost=3, attack=2, life=3, sigils=['bifurcate',''], blank_cost=blank_cost)

class BoppitW(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Boppit Worm', cost=4, attack=3, life=5, sigils=['split',''], blank_cost=blank_cost)

class Ouroboros(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        [oro_attack, oro_life] = QoL.read_data([['ouroboros', 'attack'], ['ouroboros', 'life']])
        super().__init__(species='Ouroboros', cost=2, attack=oro_attack, life=oro_life, sigils=['unkillable',''], blank_cost=blank_cost)

    def die(self) :
        self.base_attack += 1
        self.base_life += 1
        QoL.write_data([(['ouroboros', 'attack'], self.base_attack), (['ouroboros', 'life'], self.base_life)])
        super().die()

class Cockroach(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Cockroach', cost=2, attack=1, life=1, sigils=['unkillable',''], blank_cost=blank_cost)

class Stoat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Stoat', cost=1, attack=1, life=3, blank_cost=blank_cost)

class Wolf(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Wolf', cost=2, attack=3, life=2, blank_cost=blank_cost)

class Grizzly(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Grizzly', cost=3, attack=4, life=6, blank_cost=blank_cost)

class Urayuli(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Urayuli', cost=4, attack=7, life=7, blank_cost=blank_cost)

class Raven(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Raven', cost=2, attack=2, life=3, sigils=['airborne',''], blank_cost=blank_cost)

class Bee(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigils=['airborne','']) :
        super().__init__(species='Bee', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Bullfrog(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Bullfrog', cost=1, attack=1, life=2, sigils=['mighty leap',''], blank_cost=blank_cost)

class BlackGoat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Black Goat', cost=1, attack=0, life=1, sigils=['worthy sacrifice',''], blank_cost=blank_cost)

class Beehive(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Beehive', cost=1, attack=0, life=2, sigils=['bees within',''], blank_cost=blank_cost)

class Cat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Cat', cost=1, attack=0, life=1, sigils=['many lives',''], blank_cost=blank_cost)
        self.spent_lives = 0
    
    def reset_stats(self):
        super().reset_stats()
        self.spent_lives = 0

class UndeadCat(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Undead Cat', cost=1, attack=3, life=6, blank_cost=blank_cost)

class MooseBuck(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        if random.randint(0,1) == 0 :
            sigil_direction = ['hefty (left)','']
        else :
            sigil_direction = ['hefty (right)','']
        super().__init__(species='Moose Buck', cost=4, attack=3, life=7, sigils=sigil_direction, blank_cost=blank_cost)

class Dam(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=True) :
        super().__init__(species='Dam', cost=0, attack=0, life=2, blank_cost=blank_cost)

class Vole(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigils=None) :
        super().__init__(species='Vole', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Warren(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Warren', cost=1, attack=0, life=2, sigils=['vole hole',''], blank_cost=blank_cost)

class Beaver(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Beaver', cost=2, attack=1, life=3, sigils=['dam builder',''], blank_cost=blank_cost)

class Adder(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Adder', cost=2, attack=1, life=1, sigils=['touch of death',''], blank_cost=blank_cost)

class CorpseMaggots(card.BlankCard) : # in Leshy's 1 cost and the player's 2 cost groups due to the 3 cost mainly being a deterrent for the player
    def __init__(self, blank_cost=False) :
        super().__init__(species='Corpse Maggots', cost=3, attack=1, life=2, sigils=['corpse eater',''], blank_cost=blank_cost)

class Otter(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Otter', cost=1, attack=1, life=1, sigils=['waterborne',''], blank_cost=blank_cost)

class BullShark(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Bull Shark', cost=3, attack=4, life=2, sigils=['waterborne',''], blank_cost=blank_cost)

class Kingfisher(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        super().__init__(species='Kingfisher', cost=1, attack=1, life=1, sigils=['airborne','waterborne'], blank_cost=blank_cost)

class Pronghorn(card.BlankCard) :
    def __init__(self, blank_cost=False) :
        if random.randint(0,1) == 0 :
            sigils = ['lane shift right', 'bifurcate']
        else :
            sigils = ['lane shift left', 'bifurcate']
        super().__init__(species='Pronghorn', cost=2, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Salmon(card.BlankCard) : 
    def __init__(self, blank_cost=False) :
        if random.randint(0,1) == 0 :
            sigils = ['waterborne', 'lane shift right']
        else :
            sigils = ['waterborne', 'lane shift left']
        super().__init__(species='Salmon', cost=2, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Louis(card.BlankCard) : # death card
    def __init__(self, blank_cost=False) :
        if random.randint(0,1) == 0 :
            sigils = ['waterborne', 'lane shift right']
        else :
            sigils = ['waterborne', 'lane shift left']
        super().__init__(species='Louis', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class FlawPeacock(card.BlankCard) : # death card, referencing Flawed Peacock's video on Inscryption, which is how I found out about it
    def __init__(self, blank_cost=False) :
        super().__init__(species='Flaw Peacock', cost=3, attack=3, life=2, sigils=['bees within', 'many lives'], blank_cost=blank_cost)

# Allowed cards:
Poss_Playr = {
    0 : [Rabbit(), Shrew(), BlackGoat()],
    1 : [DumpyTF(), Turtle(), Stoat(), Bullfrog(), Beehive(), Cat(), Warren(), Otter(), Kingfisher(), Louis()],
    2 : [Ouroboros(), Asp(), Falcon(), Cockroach(), Wolf(), Raven(), Beaver(), Adder(), CorpseMaggots(), Pronghorn(), Salmon()],
    3 : [Lobster(), Grizzly(), BullShark(), FlawPeacock()],
    4 : [BoppitW(), Urayuli(), MooseBuck()]
}
Poss_Leshy = {
    0 : [OppositeRabbit(True), OppositeShrew(True)],
    1 : [DumpyTF(True), Turtle(True), Stoat(True), Bullfrog(True), CorpseMaggots(True), Otter(True), Kingfisher(True)],
    2 : [Asp(True), Falcon(True), Cockroach(True), Wolf(True), Raven(True), Adder(True), Pronghorn(True), Salmon(True)],
    3 : [Lobster(True), Grizzly(True), BullShark(True), BoppitW(True)]
}

Rare_Cards = [Ouroboros(), Louis(), Urayuli(), FlawPeacock()]

# categories for Leshy's AI
AI_categories = [
    # good against airbornes (glass cannons and those with mighty leap)
    {
        'category' : 'anti_air', 
        'self sigils' : ['mighty leap'],
        'opp sigils' : ['airborne'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= 3 and self_life <= opp_attack)
        },
    # good against deathtouch (waterbornes and those with deathtouch)
    {
        'category' : 'anti_deathtouch',
        'self sigils' : ['waterborne','touch of death'],
        'opp sigils' : ['touch of death'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : False)
        },
    # good against waterbornes (tanks and those with waterborne)
    {
        'category' : 'anti_water',
        'self sigils' : ['waterborne'],
        'opp sigils' : ['waterborne'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_life >= opp_attack * 3)
        },
    # good against bifurcates (glass cannons)
    {
        'category' : 'anti_bifurcate',
        'self sigils' : ['touch of death','venom'],
        'opp sigils' : ['bifurcate'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= 3 and self_life <= opp_attack)
        },
    # good against those with on hurt effects (pure tanks, airbornes, and bifurcates)
    {
        'category' : 'wont_hurt',
        'self sigils' : ['airborne','bifurcate'],
        'opp sigils' : ['bees within','split','unkillable'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack == 0)
        },
    # good against those with venom (tanks and waterbornes)
    {
        'category' : 'anti_venom',
        'self sigils' : ['waterborne'],
        'opp sigils' : ['venom'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_life >= opp_attack * 2 + 2)
        },
    # good against those moving right (heavy hitters, moves with, and bifurcate)
    {
        'category' : 'anti_right',
        'self sigils' : ['lane shift right','hefty (right)', 'bifurcate'],
        'opp sigils' : ['lane shift right','hefty (right)'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= opp_life)
        },
    # good against those moving left (heavy hitters, moves with, and bifurcate)
    {
        'category' : 'anti_left',
        'self sigils' : ['lane shift left','hefty (left)', 'bifurcate'],
        'opp sigils' : ['lane shift left','hefty (left)'],
        'stats' : (lambda self_attack, self_life, opp_attack, opp_life : self_attack >= opp_life)
        },
]

if __name__ == '__main__' :
    import deck
    Leshy_cardlist = deck.Deck([])
    for cost in Poss_Leshy :
        for card in Poss_Leshy[cost] :
            Leshy_cardlist.add_card(card)

    Player_cardlist = deck.Deck([])
    for cost in Poss_Playr :
        for card in Poss_Playr[cost] :
            if card not in Player_cardlist.cards :
                Player_cardlist.add_card(card)

    QoL.clear()
    print(QoL.center_justified('Leshy Card List'))
    print()
    print(Leshy_cardlist)
    print()
    print(QoL.center_justified('Player Card List'))
    print()
    print(Player_cardlist)