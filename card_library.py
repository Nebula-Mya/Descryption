import card
import QoL
import random

class Squirrel(card.BlankCard) :
    '''
    A squirrel card, which can be used as a resource to play other cards.
    '''
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Squirrel', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Rabbit(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['lane shift right','']) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)
    
class OppositeRabbit(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False, sigils=['lane shift left','']) :
        super().__init__(species='Rabbit', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Shrew(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['lane shift left','']) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class OppositeShrew(card.BlankCard) : # only for Leshy
    def __init__(self, blank_cost=False, sigils=['lane shift right','']) :
        super().__init__(species='Shrew', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class DumpyTF(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Dumpy Tree Frog', cost=1, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Turtle(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Turtle', cost=1, attack=0, life=4, sigils=sigils, blank_cost=blank_cost)

class Asp(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['venom','']) :
        super().__init__(species='Asp', cost=2, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Falcon(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['airborne','']) :
        super().__init__(species='Falcon', cost=2, attack=3, life=1, sigils=sigils, blank_cost=blank_cost)

class Lobster(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['bifurcate','']) :
        super().__init__(species='Lobster', cost=3, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class BoppitW(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['split','']) :
        super().__init__(species='Boppit Worm', cost=4, attack=3, life=5, sigils=sigils, blank_cost=blank_cost)

class Ouroboros(card.BlankCard) :
    oro_level = QoL.read_data([['progress markers', 'ouro level']])[0]
    def __init__(self, blank_cost=False, sigils=['unkillable','']) :
        super().__init__(species='Ouroboros', cost=2, attack=Ouroboros.oro_level, life=Ouroboros.oro_level, sigils=sigils, blank_cost=blank_cost)

    def die(self) :
        @classmethod
        def level_up(cls) :
            cls.oro_level += 1
        self.base_attack += 1
        self.base_life += 1
        level_up()
        QoL.write_data([(['progress markers', 'ouro level'], Ouroboros.oro_level)])
        super().die()

class Cockroach(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['unkillable','']) :
        super().__init__(species='Cockroach', cost=2, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Stoat(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Stoat', cost=1, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Wolf(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Wolf', cost=2, attack=3, life=2, sigils=sigils, blank_cost=blank_cost)

class Grizzly(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Grizzly', cost=3, attack=4, life=6, sigils=sigils, blank_cost=blank_cost)

class Urayuli(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Urayuli', cost=4, attack=7, life=7, sigils=sigils, blank_cost=blank_cost)

class Raven(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['airborne','']) :
        super().__init__(species='Raven', cost=2, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class Bee(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigils=['airborne','']) :
        super().__init__(species='Bee', cost=0, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Bullfrog(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['mighty leap','']) :
        super().__init__(species='Bullfrog', cost=1, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class BlackGoat(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['worthy sacrifice','']) :
        super().__init__(species='Black Goat', cost=1, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Beehive(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['bees within','']) :
        super().__init__(species='Beehive', cost=1, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Cat(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['many lives','']) :
        super().__init__(species='Cat', cost=1, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)
        self.spent_lives = 0
    
    def reset_stats(self):
        super().reset_stats()
        self.spent_lives = 0

class UndeadCat(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Undead Cat', cost=1, attack=3, life=6, sigils=sigils, blank_cost=blank_cost)

class MooseBuck(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['hefty (left)','']) :
        if random.randint(0,1) == 0 :
            sigil_direction = ['hefty (left)', sigils[1]]
        else :
            sigil_direction = ['hefty (right)', sigils[1]]
        super().__init__(species='Moose Buck', cost=4, attack=3, life=7, sigils=sigil_direction, blank_cost=blank_cost)

class Dam(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=True, sigils=['','']) :
        super().__init__(species='Dam', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Vole(card.BlankCard) : # only given by a sigil
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Vole', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Warren(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['vole hole','']) :
        super().__init__(species='Warren', cost=1, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class Beaver(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['dam builder','']) :
        super().__init__(species='Beaver', cost=2, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Adder(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['touch of death','']) :
        super().__init__(species='Adder', cost=2, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class CorpseMaggots(card.BlankCard) : # in Leshy's 1 cost and the player's 2 cost groups due to the 3 cost mainly being a deterrent for the player
    def __init__(self, blank_cost=False, sigils=['corpse eater','']) :
        super().__init__(species='Corpse Maggots', cost=3, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class Otter(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['waterborne','']) :
        super().__init__(species='Otter', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class BullShark(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['waterborne','']) :
        super().__init__(species='Bull Shark', cost=3, attack=4, life=2, sigils=sigils, blank_cost=blank_cost)

class Kingfisher(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['airborne','waterborne']) :
        super().__init__(species='Kingfisher', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class Pronghorn(card.BlankCard) :
    def __init__(self, blank_cost=False, sigils=['lane shift right','bifurcate']) :
        if random.randint(0,1) == 0 :
            sigils = ['lane shift right', 'bifurcate']
        else :
            sigils = ['lane shift left', 'bifurcate']
        super().__init__(species='Pronghorn', cost=2, attack=1, life=3, sigils=sigils, blank_cost=blank_cost)

class Salmon(card.BlankCard) : 
    def __init__(self, blank_cost=False, sigils=['waterborne','lane shift right']) :
        if random.randint(0,1) == 0 :
            sigils = ['waterborne', 'lane shift right']
        else :
            sigils = ['waterborne', 'lane shift left']
        super().__init__(species='Salmon', cost=2, attack=2, life=2, sigils=sigils, blank_cost=blank_cost)

class Louis(card.BlankCard) : # death card
    def __init__(self, blank_cost=False, sigils=['waterborne','lane shift right']) :
        if random.randint(0,1) == 0 :
            sigils = ['waterborne', 'lane shift right']
        else :
            sigils = ['waterborne', 'lane shift left']
        super().__init__(species='Louis', cost=1, attack=1, life=1, sigils=sigils, blank_cost=blank_cost)

class FlawPeacock(card.BlankCard) : # death card, referencing Flawed Peacock's video on Inscryption, which is how I found out about it
    def __init__(self, blank_cost=False, sigils=['bees within','many lives']) :
        super().__init__(species='Flaw Peacock', cost=3, attack=3, life=2, sigils=sigils, blank_cost=blank_cost)

class PlyrDeathCard1(card.BlankCard) : # death card
    def __init__(self, blank_cost=False) :
        data_to_read = [
                    ['death cards', 'first', 'name'],
                    ['death cards', 'first', 'attack'],
                    ['death cards', 'first', 'life'],
                    ['death cards', 'first', 'cost'],
                    ['death cards', 'first', 'sigils'],
                    ['death cards', 'first', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter = death_easter

class PlyrDeathCard2(card.BlankCard) : # death card
    def __init__(self, blank_cost=False) :
        data_to_read = [
                    ['death cards', 'second', 'name'],
                    ['death cards', 'second', 'attack'],
                    ['death cards', 'second', 'life'],
                    ['death cards', 'second', 'cost'],
                    ['death cards', 'second', 'sigils'],
                    ['death cards', 'second', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter = death_easter

class PlyrDeathCard3(card.BlankCard) : # death card
    def __init__(self, blank_cost=False) :
        data_to_read = [
                    ['death cards', 'third', 'name'],
                    ['death cards', 'third', 'attack'],
                    ['death cards', 'third', 'life'],
                    ['death cards', 'third', 'cost'],
                    ['death cards', 'third', 'sigils'],
                    ['death cards', 'third', 'easter']
                ]
        [death_name, death_attack, death_life, death_cost, death_sigils, death_easter] = QoL.read_data(data_to_read)
        super().__init__(species=death_name, cost=death_cost, attack=death_attack, life=death_life, sigils=death_sigils, blank_cost=blank_cost)
        self.easter = death_easter

class RabbitPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Rabbit Pelt', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class WolfPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Wolf Pelt', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class GoldenPelt(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Golden Pelt', cost=0, attack=0, life=3, sigils=sigils, blank_cost=blank_cost)

class Smoke(card.BlankCard) : # only given in campaign
    def __init__(self, blank_cost=False, sigils=['worthy sacrifice', '']) : # will have the bone king sigil once bones are implemented
        super().__init__(species='The Smoke', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class Coyote(card.BlankCard) : # only used by prospector until bones are implemented
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Coyote', cost=2, attack=2, life=1, sigils=sigils, blank_cost=blank_cost)

class PackMule(card.BlankCard) : # only used by prospector
    def __init__(self, blank_cost=False, sigils=['lane shift right','']) :
        super().__init__(species='Pack Mule', cost=0, attack=0, life=5, sigils=sigils, blank_cost=blank_cost)

class Bloodhound(card.BlankCard) : 
    def __init__(self, blank_cost=False, sigils=['','']) : # will have guardian sigil once implimented
        super().__init__(species='Bloodhound', cost=2, attack=2, life=3, sigils=sigils, blank_cost=blank_cost)

class GoldNugget(card.BlankCard) : # only used by prospector
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Gold Nugget', cost=0, attack=0, life=2, sigils=sigils, blank_cost=blank_cost)

class BaitBucket(card.BlankCard) : # only used by angler
    def __init__(self, blank_cost=False, sigils=['','']) :
        super().__init__(species='Bait Bucket', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

class StrangeFrog(card.BlankCard) : # only used by trapper
    def __init__(self, blank_cost=False, sigils=['mighty leap','']) :
        super().__init__(species='Strange Frog', cost=1, attack=1, life=2, sigils=sigils, blank_cost=blank_cost)

class LeapingTrap(card.BlankCard) : # only used by trapper
    def __init__(self, blank_cost=False, sigils=['mighty leap','steel trap']) :
        super().__init__(species='Leaping Trap', cost=0, attack=0, life=1, sigils=sigils, blank_cost=blank_cost)

# Allowed cards:
Poss_Playr = {
    0 : [Rabbit(), Shrew(), BlackGoat()],
    1 : [DumpyTF(), Turtle(), Stoat(), Bullfrog(), Beehive(), Cat(), Warren(), Otter(), Kingfisher()],
    2 : [Ouroboros(), Asp(), Falcon(), Cockroach(), Wolf(), Raven(), Beaver(), Adder(), CorpseMaggots(), Pronghorn(), Salmon(), Bloodhound()],
    3 : [Lobster(), Grizzly(), BullShark()],
    4 : [BoppitW(), Urayuli(), MooseBuck()]
}
Poss_Leshy = {
    0 : [OppositeRabbit(True), OppositeShrew(True)],
    1 : [DumpyTF(True), Turtle(True), Stoat(True), Bullfrog(True), CorpseMaggots(True), Otter(True), Kingfisher(True)],
    2 : [Asp(True), Falcon(True), Cockroach(True), Wolf(True), Raven(True), Adder(True), Pronghorn(True), Salmon(True), Bloodhound(True)],
    3 : [Lobster(True), Grizzly(True), BullShark(True), BoppitW(True)]
}
Poss_Death = [Louis(), FlawPeacock(), PlyrDeathCard1(), PlyrDeathCard2(), PlyrDeathCard3()]
Rare_Cards = [Ouroboros(), Urayuli(), MooseBuck(), BullShark(), BoppitW()]

# Tribes
Reptiles = [Bullfrog(), DumpyTF(), Turtle(), Adder(), Asp(), Ouroboros(), StrangeFrog()] # also includes amphibians for accuracy to Inscryption
Insects = [BoppitW(), Beehive(), Bee(), Cockroach(), CorpseMaggots()]
Avians = [Kingfisher(), Falcon(), Raven()]
Canines = [Wolf(), Bloodhound(), Coyote()]
Hooved = [BlackGoat(), MooseBuck(), Pronghorn(), PackMule()]
Squirrels = [Squirrel()]

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
        'opp sigils' : ['bees within','split','unkillable', 'steel trap'],
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
        for card_ in Poss_Leshy[cost] :
            Leshy_cardlist.add_card(card_)

    Player_cardlist = deck.Deck([])
    for cost in Poss_Playr :
        for card_ in Poss_Playr[cost] :
            if card_ not in Player_cardlist.cards :
                Player_cardlist.add_card(card_)

    QoL.clear()
    print(QoL.center_justified('Leshy Card List'))
    print()
    print(Leshy_cardlist)
    print()
    print(QoL.center_justified('Player Card List'))
    print()
    print(Player_cardlist)