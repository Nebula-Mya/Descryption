import sigils
import os
import QoL

class BlankCard() :
    '''
    An empty card, serves both as an empty zone and as the parent class for all other cards

    Arguments :
        species : the species of the card (str)
        cost : number of sacrifices needed for summoning (int)
        attack : base attack stat (int)
        life : base life stat (int)
        sigil : the sigil the card currently has (str)
        status : whether the card is alive or dead (str)
        zone : the zone the card is in, with 0 as default (int)
        blank_cost : whether the card has a blank cost (bool)
        blank_stats : whether the card has blank stats (bool)
    
    Other Attributes :
        name : the name of the card for displaying, with padding and abbreviation (str)
        is_poisoned : whether the card is poisoned (bool)
        saccs : the cost without formatting (int)
        base_attack : the base attack stat (int)
        current_attack : the current attack stat (int)
        base_life : the base life stat (int)
        current_life : the current life stat (int)
        text_lines : the ASCII art for the card split by line (list)
        line_cursor : the current line to print (int)

    Methods :
        reset_stats() : sets current stats to base stats
        attack(front_left_card, front_card, front_right_card, left_card, right_card) : attacks zone(s) in front
        print() : prints self.name
        text_by_line() : returns one line of the card's ASCII art at a time
        take_damage(damage) : reduces current life by damage 
        play(zone) : activates sigils on entering field, resets stats, and updates zone
        die() : resets stats and updates ASCII
        explain() : prints explanation of stats and sigil for player
        update_ASCII() : updates the ASCII art for the card
    '''
    def __init__(self, species = '', cost = 0, attack = 0, life = 0, sigil = '', status = 'alive', zone = 0, blank_cost = False, blank_stats = False) :

        # basic variables
        self.is_poisoned = False
        self.species = species
        self.saccs = cost
        self.base_attack = attack
        self.current_attack = attack
        self.base_life = life
        self.current_life = life
        self.sigil = sigil
        self.status = status
        self.zone = zone
        self.blank_cost = blank_cost
        self.blank_stats = blank_stats

        # create name for displaying card
        if species == '' or blank_cost : # takes advantage of extra space from having no cost
            self.name = species.ljust(12)[:12]
        else :
            self.name = species.ljust(9)[:9]
            
        # abbreviate name if it is too long
        if len(self.name) >= len(species) : # guard clause
            pass
        elif self.name[-2] == ' ' :
            self.name = self.name[:-2] + '. '
        else :
            self.name = self.name[:-1] + '.'
        
        # create ASCII art for card
        self.update_ASCII()
        
    def reset_stats(self) :
        '''
        resets current stats to base stats
        '''
        self.zone = 0
        self.status = 'alive'
        self.is_poisoned = False
        self.current_attack = self.base_attack
        self.current_life = self.base_life
        self.update_ASCII()

    def attack(self, front_left_card, front_card, front_right_card, hand, is_players=False, bushes={}) :
        '''
        attacks zone(s) in front

        Arguments:
            front_left_card: the card in the zone to the left of the front card (card object)
            front_card: the card in the zone in front of the attacking card (card object)
            front_right_card: the card in the zone to the right of the front card (card object)
            hand: the player's hand (list)
            is_players: whether the attacking card is on the player's field (bool)
            bushes: the dict of bushed cards (dict)
        
        Returns:
            points: the damage dealt to the opponent (int)
        '''
        # set up variables
        points = 0

        # attack cards
        if self.sigil in sigils.on_attacks : # if sigil is a sigil that activates on attack
            [points] = QoL.exec_sigil_code(self, sigils.on_attacks, local_vars=locals(), vars_to_return=['points'])
        else : # if sigil is irrelevant or none existent, attack front
            points = front_card.take_damage(self.current_attack, hand, in_opp_field=is_players, bushes=bushes)
        
        # if poisoned, deal 1 damage to self
        if self.is_poisoned :
            self.take_damage(1, hand)

        return points

    def __str__(self) :
        return self.name

    def text_by_line(self) :
        '''
        returns one line of the card's ASCII art at a time
        '''
        self.line_cursor += 1
        if self.line_cursor == 13 : 
            self.line_cursor = 2
        return self.text_lines[self.line_cursor - 1]

    def take_damage(self, damage, hand, from_air=False, in_opp_field=False, in_bushes=False, bushes={}, deathtouch=False) :
        '''
        reduces current life by damage

        Arguments:
            damage: the amount of damage to take (int)
            hand: the player's hand (list)
            from_air: whether the damage is from an airborne creature (bool)
            in_opp_field: whether the card is on Leshy's feild (bool)
            in_bushes: whether the card is in the bushes (bool)
            bushes: the dict of bushed cards (dict)
            deathtouch: whether the damage is from a deathtouch creature (bool)

        Returns:
            teeth: damage to controller (int)
        '''
        # set up variables
        teeth = 0

        # take damage
        if self.sigil in sigils.on_damages: # if sigil is a sigil that activates on damage
            [teeth] = QoL.exec_sigil_code(self, sigils.on_damages, local_vars=locals(), vars_to_return=['teeth'])
        # if sigil is irrelevant or none existent, take damage
        elif self.species == '' or self.status == 'dead' or from_air : 
            teeth = damage
        else :
            prev_life = self.current_life
            self.current_life -= damage
            self.update_ASCII()
            if self.current_life <= 0 or deathtouch :
                self.status = 'dead'
                if in_opp_field and self.current_life <= 0 :
                    excess_damage = damage - prev_life
                    bushes[self.zone].take_damage(excess_damage, hand, in_bushes=True)
        
        return teeth     

    def play(self, zone) :
        '''
        activates sigils on entering field, resets stats, and updates zone
        '''
        if zone not in range (1, 6) : # error handling
            raise ValueError('Zone must be between 1 and 5')
        self.reset_stats()
        self.zone = zone
        self.update_ASCII()

    def die(self) :
        '''
        resets stats and updates ASCII
        '''
        self.reset_stats()
        self.update_ASCII()

    def explain(self) :
        '''
        prints explanation of stats and sigil for player
        '''
        # set up variables
        explanation = ''

        # get terminal size
        term_cols = os.get_terminal_size().columns
        card_gaps = (term_cols*55 // 100) // 5 - 15

        # get sigil name
        match self.sigil :
            case '' :
                sigil_text = 'No Sigil'
            case _ if 'hefty' in self.sigil:
                sigil_text = 'Hefty:'
            case _ :
                sigil_text = QoL.title_case(self.sigil) + ':'

        # get parameters for sigil description
        max_desc_first = term_cols - 18 - card_gaps*2 - len(sigil_text)
        max_desc_rest = term_cols - 14 - card_gaps*2

        # split description into lines
        [desc_first_line, desc_second_line, desc_third_line] = QoL.split_nicely(sigils.Dict[self.sigil][1], max_desc_first, max_desc_rest, max_lines=3, add_blank_lines=True)
        
        # create display text
        for line in range(1, 12) :
            if line != 1 : # go to next line
                explanation += '\n'
            explanation += ' '*card_gaps + self.text_lines[line] # add the card line
            match line : # add the explanation to the end of the line
                case 2 : # cost and species
                    explanation += ' '*(card_gaps + 2) + self.species + ' requires ' + str(self.saccs) + ' sacrifices to summon.'
                case 6 : # sigil and description line 1
                    explanation += ' '*(card_gaps + 2) + sigil_text + ' ' + desc_first_line
                case 7 : # description line 2
                    explanation += ' '*(card_gaps + 6) + desc_second_line
                case 8 : # description line 3
                    explanation += ' '*(card_gaps + 6) + desc_third_line
                case 10 : # stats
                    explanation += ' '*(card_gaps + 2) + self.species + ' has an attack power of ' + str(self.current_attack) + ' and life points of ' + str(self.current_life) + ' of ' + str(self.base_life) + '.'

        print(explanation)

    def update_ASCII(self) :
        '''
        updates the ASCII art for the card
        '''
        # reset line cursor
        self.line_cursor = 1

        # update cost and stats for displaying card
        if self.blank_cost or self.species == '':
            self.cost = ''
        else :
            self.cost = str("C:" + str(self.saccs))
        
        if self.blank_stats or self.species == '':
            self.stats = ' '*3
        else :
            self.stats = hex(self.current_attack % 16)[2] + "/" + hex(self.current_life % 16)[2]
        
        # update ASCII art for card
        self.text_lines = '''
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
    '''.format(species=self.name, C=self.cost, rw1=sigils.Dict[self.sigil][0][0], rw2=sigils.Dict[self.sigil][0][1], rw3=sigils.Dict[self.sigil][0][2], S=self.stats).split("\n")

if __name__ == "__main__" :
    testblank = BlankCard()
    testsigil = slot4 = BlankCard(species='test',cost=3,attack=1,life=2,sigil='bifurcate')
    print()
    print('Blank Card')
    print(testblank.text_lines)
    print(len(testblank.text_lines))
    testblank.explain()