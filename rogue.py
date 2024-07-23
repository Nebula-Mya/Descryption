import deck
import duel
import QoL
import card_library
import ASCII_text
import card
import random
import sigils
import os
import bosses

class rogue_campaign :
    '''
    the current campaign data, such as the current level, the current decks, teeth (money), progress in the level, candles, etc.
    
    Attributes:
        level: the current level of the campaign (int)
        progress: the current progress in the level (int)
        player_deck: the player's deck (deck.Deck)
        squirrel_deck: the squirrel deck (deck.Deck)
        teeth: the player's money (int)
        lives: the player's lives (int)
        dead_campfire : if the survivors have been poisoned (bool)

    Methods:
        add_teeth: adds teeth to the player's total
        add_life: adds a life to the player's total
        remove_life: removes a life from the player's total
        add_card: adds a card to the player's deck
        remove_card: removes a card from the player's deck
        change_sigil: changes the sigil of a card in the player's deck
        shuffle_deck: shuffles the player's deck
        print_deck: prints the player's deck
    '''
    def __init__(self, start_decklist, start_teeth=0, lives=2) :
        '''
        initializes the campaign object
        
        Arguments:
            start_decklist: the starting decklist for the player (list)
            start_teeth: the starting amount of teeth for the player, defaults to 0 (int)
            lives: the starting amount of lives for the player, defaults to 2 (int)
        '''
        self.level = 0
        self.progress = 0
        self.player_deck = deck.Deck(start_decklist)
        self.squirrel_deck = duel.resource_gen(10)
        self.teeth = start_teeth
        self.lives = lives
        self.dead_campfire = False

    def add_teeth(self, amount) :
        self.teeth += amount
    
    def add_life(self) :
        self.lives += 1
    
    def remove_life(self) :
        self.lives -= 1
        if self.lives <= 0 :
            lost_run(self)

    def add_card(self, card) :
        '''
        adds a card to the player's deck
        
        Arguments:
            card: the card to add to the player's deck (card object)
        '''
        self.player_deck.add_card(card)

    def remove_card(self, card) :
        '''
        removes a card from the player's deck
        
        Arguments:
            index: the index of the card to remove (int)
        '''
        sorted_deck = QoL.sort_deck(self.player_deck.cards)
        index = sorted_deck.index(card)
        self.player_deck.remove_card(index)

    def add_sigil(self, card, sigil) :
        '''
        changes the sigil of a card in the player's deck
        
        Arguments:
            card: the card to change the sigil of (card object)
            sigil: sigil to change to (str)
        '''
        sorted_deck = QoL.sort_deck(self.player_deck.cards)
        index = sorted_deck.index(card)

        if card.has_sigil(sigil) :
            raise ValueError(f'Card already has sigil {sigil}')
        elif not card.has_sigil('') :
            raise ValueError('Card already has two sigils')
        
        sigil_slot = card.sigils.index('')
        
        self.player_deck.change_sigil(index, sigil, sigil_slot)
    
    def shuffle_deck(self) :
        return self.player_deck.shuffle()
    
    def print_deck(self) :
        print(self.player_deck)

    def has_lost(self) :
        return self.lives <= 0

def card_equation(card1, card2, result) :
    '''
    generate the display text for combining cards

    Arguments:
        card1: the first card (card object)
        card2: the second card (card object)
        result: the resulting card (card object)
    
    Returns:
        lines: the display text for combining the cards (list[str])
    '''
    # set up variables
    plus_lines = '''{blank_lines}{spc}  |  {spc}
{spc}――|――{spc}
{spc}  |  {spc}
{blank_lines}'''.format(blank_lines=(' '*9 + '\n')*5, spc=' '*2).split('\n')
    equals_lines = '''{blank_lines}{spc}_____{spc}
{spc}     {spc}
{spc}‾‾‾‾‾{spc}
{blank_lines}'''.format(blank_lines=(' '*9 + '\n')*5, spc=' '*2).split('\n')
    card1_lines = card1.text_lines
    card2_lines = card2.text_lines
    result_lines = result.text_lines
    
    # combine the lines
    new_lines = [card1_lines[i] + plus_lines[i] + card2_lines[i] + equals_lines[i] + result_lines[i] for i in range(1,12)]

    return new_lines

def card_battle(campaign, Poss_Leshy=None) : 
    '''
    starts a card battle between the player and Leshy, with the player's deck being campaign.player_deck
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
        Poss_Leshy: the possible cards for Leshy's deck, defaults to all allowed Leshy cards with costs <= to player's max cost (list)

    Returns:
        bool: True if the player wins, False if the player loses
    '''
    def gameplay(campaign, Poss_Leshy) :
        data_to_read = [
            ['settings', 'difficulty', 'leshy median plays'],
            ['settings', 'difficulty', 'leshy plays variance'],
            ['settings', 'difficulty', 'leshy strat chance'],
            ['settings', 'difficulty', 'leshy offense threshold']
        ]
        [play_median, play_var, opp_strat, opp_threshold] = QoL.read_data(data_to_read)

        deck_size = len(campaign.player_deck.cards)

        if Poss_Leshy :
            leshy_deck = duel.deck_gen(Poss_Leshy, int(deck_size * 1.5))
        else :
            player_max_cost = max([card.saccs for card in campaign.player_deck.cards])
            fair_poss_leshy = {cost: [card for card in card_library.Poss_Leshy[cost]] for cost in range(0, player_max_cost)} # may be changed later for balancing
            leshy_deck = duel.deck_gen(fair_poss_leshy, int(deck_size * 1.5))

        (_, winner, overkill, _) = duel.main(deck_size, 4, play_median, play_var, opp_strat, opp_threshold, player_deck_obj=campaign.player_deck, opponent_deck_obj=leshy_deck, squirrels_deck_obj=campaign.squirrel_deck, print_results=False)

        if winner == 'opponent' :
            campaign.remove_life()
            QoL.clear()
            print('\n'*3)
            wick_states = (campaign.lives) * [2] + [3]
            wick_states += [0] * (3 - len(wick_states))
            ASCII_text.print_candelabra(wick_states)
            print()
            input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
            return False
        
        campaign.add_teeth(overkill)
        QoL.clear()
        print('\n'*3)
        wick_states = (campaign.lives) * [2]
        wick_states += [0] * (3 - len(wick_states))
        ASCII_text.print_candelabra(wick_states)
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
        return True
    
    return gameplay(campaign, Poss_Leshy) # add flavor text, context, etc.

def card_choice(campaign) : 
    '''
    allows the player to choose a card to add to their deck from a list of 3, with the list being generated from different card categories

    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    def card_choice(campaign, cards) : # choose a card from a list of 3 and add it to the player's deck
        # set up variables
        invalid_choice = False

        while True :
            # print the available cards and options
            QoL.clear()
            print('\n'*5)
            print(QoL.center_justified('Available cards:'))
            QoL.print_deck(cards, numbered=True, centered=True)
            options = '''
1. View a card
2. View deck
3. Pick a card
'''
            print(QoL.center_justified(options, blocked=True))

            if invalid_choice :
                print(QoL.center_justified('Invalid choice') + '\n')
                invalid_choice = False
            else :
                print('\n')

            # get the user's choice
            choice = input(QoL.center_justified(' '*2 + 'Choose an option:').rstrip() + ' ')

            match choice :
                case '1' : # view a card
                    # print the available cards and options
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Available cards:'))
                    QoL.print_deck(cards, numbered=True, centered=True)
                    options = '''
1. View a card
2. View deck
3. Pick a card

'''
                    print(QoL.center_justified(options, blocked=True))

                    # get the user's choice
                    card_index = input(QoL.center_justified('Enter the number of the card to view:').rstrip() + ' ')
                    (is_int, card_index) = QoL.reps_int(card_index, -1)

                    if is_int and card_index in range(3) :
                        QoL.clear()
                        print('\n'*5)
                        print(QoL.center_justified('Available cards:'))
                        QoL.print_deck(cards, numbered=True, centered=True)
                        print()
                        cards[card_index].explain()
                        input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')
                    
                    else :
                        invalid_choice = True
                
                case '2' :
                    # print the player's deck
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Your deck:'))
                    campaign.print_deck()
                    print()
                    input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')
                
                case '3' :
                    # print the available cards and options
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Available cards:'))
                    QoL.print_deck(cards, numbered=True, centered=True)
                    options = '''
1. View a card
2. View deck
3. Pick a card

'''
                    print(QoL.center_justified(options, blocked=True))

                    # get the user's choice
                    card_index = input(QoL.center_justified('Enter the number of the card to pick:').rstrip() + ' ')
                    (is_int, card_index) = QoL.reps_int(card_index, -1)

                    if is_int and card_index in range(3) :
                        return card_index
                    
                    else :
                        invalid_choice = True
                
                case _ :
                    invalid_choice = True

    def normal_cards(campaign) : # generate a list of 3 taken from card_library.Poss_Playr
        card_options = duel.deck_gen(card_library.Poss_Playr, 3).cards
        card_index = card_choice(campaign, card_options)
        QoL.clear()
        print('\n'*5)
        print('You chose:')
        card_options[card_index].explain()
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
        campaign.add_card(card_options[card_index])

    def cost_cards(campaign) : # generate a list of 3 taken from card_library.Poss_Cost, only seeing the costs of the cards
        card_options = duel.deck_gen(card_library.Poss_Playr, 3).cards
        card_options_hidden = [card.BlankCard(species='???', cost=option.cost[-1], sigils=['???',''], blank_stats=True) for option in card_options]
        card_index = card_choice(campaign, card_options_hidden)
        QoL.clear()
        print('\n'*5)
        print('You chose:')
        card_options[card_index].explain()
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
        campaign.add_card(card_options[card_index])

    def death_cards(campaign) : # generate a list of 3 death cards taken from card_library.Poss_Death, only available after 5 deaths
        card_options = random.sample(card_library.Poss_Death, 3)
        card_index = card_choice(campaign, card_options)
        QoL.clear()
        print('\n'*5)
        print('You chose:')
        card_options[card_index].explain()
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
        campaign.add_card(card_options[card_index])

    def rare_cards(campaign) : # generate a list of 3 rare cards taken from card_library.Rare_Cards, occurs after boss fights
        card_options = random.sample(card_library.Rare_Cards, 3)
        card_index = card_choice(campaign, card_options)
        QoL.clear()
        print('\n'*5)
        print('You chose:')
        card_options[card_index].explain()
        print()
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
        campaign.add_card(card_options[card_index])

    def gameplay(campaign) :
        choice_categories = ['normal', 'cost', 'rare']
        [wins, losses] = QoL.read_data([['progress markers', 'wins'], ['progress markers', 'losses']])
        if wins + losses >= 5 :
            choice_categories.append('death')
        
        match random.choice(choice_categories) :
            case 'normal' : normal_cards(campaign)
            case 'cost' : cost_cards(campaign)
            case 'rare' : rare_cards(campaign)
            case 'death' : death_cards(campaign)

    gameplay(campaign) # add flavor text, context, etc.

def sigil_sacrifice(campaign) : # format visuals
    '''
    allows the player to sacrifice a card to give its sigil to another card
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    def get_reciever(deck_list) :
        '''
        allows the player to choose a card to receive a sigil
        
        Arguments:
            deck_list: the list of cards to choose from (list[card object])
            
        Returns:
            card object: the card to receive the sigil
        '''
        # set up variables
        invalid_choice = False
        no_slots = False
        sorted_deck = QoL.sort_deck(deck_list)
        
        while True :
            # print the player's deck
            QoL.clear()
            QoL.print_deck(sorted_deck, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False
            elif no_slots :
                print(QoL.center_justified('That card has no open sigil slots'))
                print()
                no_slots = False

            # get user input
            card_index = input(QoL.center_justified('Enter the number of the card to receive a new sigil:').rstrip() + ' ')
            (is_int, card_index) = QoL.reps_int(card_index, -1)
            if not is_int or card_index not in range(len(sorted_deck)) :
                invalid_choice = True
                continue
            elif not sorted_deck[card_index].has_sigil('') :
                no_slots = True
                continue

            return sorted_deck[card_index]
        
    def get_sacrifice(deck_list, reciever) :
        '''
        allows the player to choose a card to sacrifice
        
        Arguments:
            deck_list: the list of cards to choose from (list[card object])
            reciever: the card to receive the sigil (card object)
            
        Returns:
            card object: the card to sacrifice
        '''
        # set up functions
        same_sigil = lambda sigil_1, sigil_2 : sigil_1 != '' and (sigil_1 == sigil_2 or all('lane shift' in sigil for sigil in [sigil_1, sigil_2]) or all('hefty' in sigil for sigil in [sigil_1, sigil_2])) # check if two sigils are the same or variations of the same sigil
        good_sigil = lambda reciever, sigil : sigil != '' and not same_sigil(reciever.sigils[0], sigil) and not same_sigil(reciever.sigils[1], sigil) # check if a sigil can be transferred
        poss_transfers = lambda reciever, sacrifice : sum([good_sigil(reciever, sigil) for sigil in sacrifice.sigils]) # check how many sigils can be transferred
        good_sigils = lambda reciever, sacrifice : poss_transfers(reciever, sacrifice) > 0 # check if any sigils can be transferred

        # set up variables
        invalid_choice = False
        deck_have_sigil = QoL.sort_deck([card_ for card_ in deck_list if good_sigils(reciever, card_)])

        while True :
            # print the player's deck with only cards that have sigils
            QoL.clear()
            QoL.print_deck(deck_have_sigil, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False

            # get user input
            card_index = input(QoL.center_justified('Enter the number of the card to sacrifice for its sigil:').rstrip() + ' ')
            (is_int, card_index) = QoL.reps_int(card_index, -1)
            if not is_int or card_index not in range(len(deck_have_sigil)) :
                invalid_choice = True
                continue

            return deck_have_sigil[card_index]

    def get_sigil_slot(reciever, sacrifice) :
        '''
        allows the player to choose which sigil to transfer
        
        Arguments:
            reciever: the card to receive the sigil (card object)
            sacrifice: the card to sacrifice (card object)
            
        Returns:
            list: the indexes of the sigils to transfer
        '''
        # set up variables
        def sigil_name(sigil) :
            match sigil :
                case '' : return 'No Sigil'
                case _ if 'hefty' in sigil : return 'Hefty'
                case _ if 'lane shift' in sigil : return 'Sprinter'
                case _ : return QoL.title_case(sigil)
        sigil_names = [sigil_name(sacrifice.sigils[i]) for i in range(2)]

        # set up functions
        same_sigil = lambda sigil_1, sigil_2 : sigil_1 != '' and (sigil_1 == sigil_2 or all('lane shift' in sigil for sigil in [sigil_1, sigil_2]) or all('hefty' in sigil for sigil in [sigil_1, sigil_2])) # check if two sigils are the same or variations of the same sigil
        good_sigil = lambda reciever, sigil : sigil != '' and not same_sigil(reciever.sigils[0], sigil) and not same_sigil(reciever.sigils[1], sigil) # check if a sigil can be transferred
        poss_transfers = lambda reciever, sacrifice : sum([good_sigil(reciever, sigil) for sigil in sacrifice.sigils]) # check how many sigils can be transferred

        match poss_transfers(reciever, sacrifice) :
            case 2 :
                # both sigils can be transferred
                if reciever.sigils == ['', ''] : return [0,1]

                # print sacrifice explanation
                invalid_choice = False

                while True :
                    # print the sacrifice card
                    QoL.clear()
                    sacrifice.explain()

                    if invalid_choice :
                        print(QoL.center_justified('Invalid choice'))
                        print()
                        invalid_choice = False

                    (is_int, sigil_index) = QoL.reps_int( input(QoL.center_justified(f'Would you like to transfer 1) {sigil_names[0]} or 2) {sigil_names[1]}? ').rstrip() + ' ' ), -1)

                    if is_int and sigil_index in range(2) :
                        return [sigil_index]
                    invalid_choice = True

            case 1 : return [1 - good_sigil(reciever, sacrifice.sigils[0])]

            case _ : raise ValueError('No sigils can be transferred')

    def confirm_choice(reciever, sacrifice, sigil_indexes) :
        '''
        allows the player to confirm their choice of cards and sigils
        
        Arguments:
            reciever: the card to receive the sigil (card object)
            sacrifice: the card to sacrifice (card object)
            sigil_indexes: the indexes of the sigil to transfer (list)
        
        Returns:
            bool: True if the player confirms their choice, False if they do not
        '''
        # set up variables
        if len(sigil_indexes) == 2 : result_sigils = sacrifice.sigils
        elif reciever.sigils[0] == '' : result_sigils = [sacrifice.sigils[sigil_indexes[0]], reciever.sigils[1]]
        else : result_sigils = [reciever.sigils[0], sacrifice.sigils[sigil_indexes[0]]]
        result_card = card.BlankCard(species=reciever.species, cost=reciever.saccs, attack=reciever.base_attack, life=reciever.base_life, sigils=result_sigils)

        # generate the equation
        equation = '\n'.join(card_equation(reciever, sacrifice, result_card))

        # print the equation
        QoL.clear()
        print(QoL.center_justified(equation, blocked=True))

        # get confirmation from the player
        confirm_input = input(QoL.center_justified('Are you sure these are the cards you want to use? (y/n)').rstrip() + ' ')

        if confirm_input.lower() != 'y' :
            return False
        
        return True

    def gameplay(campaign) :
        # set up variables
        deck_list = campaign.player_deck.cards

        while True :
            # show deck; select a card to receive the sigil
            reciever = get_reciever(deck_list)

            # show deck (filter out those without sigils); select a card to sacrifice
            sacrifice = get_sacrifice(deck_list, reciever)

            # if sacrifice has 2 sigils and the recieving card doesn't have two open slots, ask which sigil to transfer
            sigil_indexes = get_sigil_slot(reciever, sacrifice)

            # confirm the sacrifice (visually show the sigil being transferred as an addition equation)
            if not confirm_choice(reciever, sacrifice, sigil_indexes) :
                continue

            # add the sigil to the card
            for index in sigil_indexes :
                campaign.add_sigil(reciever, sacrifice.sigils[index])

            # remove the sacrificed card from the deck
            campaign.remove_card(sacrifice)

            break

    gameplay(campaign) # add flavor text, context, etc.

def merge_cards(campaign) : # format visuals
    '''
    allows the player to merge two cards of the same species into one, with the new card having combined stats and sigils
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    def select_first(deck_list) :
        '''
        allows the player to choose the first card to merge
        
        Arguments:
            deck_list: the list of cards to choose from (list[card object])
        
        Returns:
            card object: the card to merge
        '''
        # set up variables
        invalid_choice = False
        sorted_deck = QoL.sort_deck(deck_list)
        
        while True :
            # print the player's deck
            QoL.clear()
            QoL.print_deck(sorted_deck, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False

            # get user input
            card_index = input(QoL.center_justified('Enter the number of the first card to merge:').rstrip() + ' ')
            (is_int, card_index) = QoL.reps_int(card_index, -1)
            if not is_int or card_index not in range(len(sorted_deck)) :
                invalid_choice = True
                continue

            return sorted_deck[card_index]

    def select_second(deck_list, card_1) :
        '''
        allows the player to choose the second card to merge
        
        Arguments:
            deck_list: the list of cards to choose from (list[card object])
            card_1: the first card to merge (card object)
            
        Returns:
            card object: the card to merge with
        '''
        # set up variables
        invalid_choice = False
        same_species = QoL.sort_deck([card_ for card_ in deck_list if card_.species == card_1.species and card_ != card_1])

        while True :
            # print the player's deck
            QoL.clear()
            QoL.print_deck(same_species, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False

            # get user input
            card_index = input(QoL.center_justified('Enter the number of the second card to merge:').rstrip() + ' ')
            (is_int, card_index) = QoL.reps_int(card_index, -1)
            if not is_int or card_index not in range(len(same_species)) or same_species[card_index].species != card_1.species :
                invalid_choice = True
                continue

            return same_species[card_index]

    def get_sigils(card_1, card_2) :
        '''
        allows the player to choose which sigils to keep
        
        Arguments:
            card_1: the first card to merge (card object)
            card_2: the second card to merge (card object)
            
        Returns:
            list[str]: the sigils to keep
        '''
        def sigil_name(sigil) :
            match sigil :
                case '' : return 'No Sigil'
                case _ if 'hefty' in sigil : return 'Hefty'
                case _ if 'lane shift' in sigil : return 'Sprinter'
                case _ : return QoL.title_case(sigil)

        unique_sigils = []
        for sigil in card_1.sigils + card_2.sigils :
            if sigil != '' and not any(sigil_name(sigil) == sigil_name(sigil_) for sigil_ in unique_sigils) :
                unique_sigils.append(sigil)

        if len(unique_sigils) <= 2 : # if there are 2 or fewer unique sigils, return all sigils
            if len(unique_sigils) < 2 : # make sure there are 2 sigils
                unique_sigils += [''] * (2 - len(unique_sigils))
            
            return unique_sigils
        
        # set up variables
        all_sigils = [sigil for sigil in card_1.sigils + card_2.sigils if sigil != '']
        options = '\n' + '\n'.join([f'{i+1}. {sigil_name(sigil)}: {sigils.Dict[sigil][1]}' for i, sigil in enumerate(all_sigils)]) + '\n'
        invalid_choice = False
        iter = -1
        iter_names = ['first', 'second']
        final_sigils = []

        while True :
            # print the sigils and their effects
            QoL.clear()
            print(QoL.center_justified('Sigils to choose from:'))
            print(QoL.center_justified(options, blocked=True))

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False
            else :
                iter += 1

            # get user input
            sigil_index = input(QoL.center_justified(f'Enter the number of the {iter_names[iter]} sigil to keep:').rstrip() + ' ')
            (is_int, sigil_index) = QoL.reps_int(sigil_index, -1)

            if not is_int or sigil_index not in range(len(all_sigils)) :
                invalid_choice = True
                continue

            final_sigils.append(all_sigils[sigil_index])

            if iter > 0 :
                return final_sigils

    def confirm_choice(card_1, card_2, result_sigils) :
        '''
        allows the player to confirm their choice of cards and sigils
        
        Arguments:
            card_1: the first card to merge (card object)
            card_2: the second card to merge (card object)
            result_sigils: the sigils to keep (list[str])
            
        Returns:
            bool: True if the player confirms their choice, False if they do not
            result: the resulting card (card object)
        '''
        # set up variables
        result = {
            'species': card_1.species,
            'cost': card_1.saccs + card_2.saccs,
            'attack': card_1.base_attack + card_2.base_attack,
            'life': card_1.base_life + card_2.base_life,
            'sigils': result_sigils
        }
        card_result = card.BlankCard(**result)

        # generate the equation
        equation = '\n'.join(card_equation(card_1, card_2, card.BlankCard(**result)))

        # print the equation
        QoL.clear()
        print(QoL.center_justified(equation, blocked=True))

        # get confirmation from the player
        confirm_input = input(QoL.center_justified('Are you sure these are the cards you want to use? (y/n)').rstrip() + ' ')

        if confirm_input.lower() != 'y' :
            return False, None
        
        return True, card_result

    def gameplay(campaign) :
        # set up variables
        deck_list = campaign.player_deck.cards

        while True :
            # show deck (numbered); select a card to merge
            card_1 = select_first(deck_list)

            # show cards of the same species; select a card to merge with
            card_2 = select_second(deck_list, card_1)

            # if more than 2 unique sigils, ask which sigils to keep
            result_sigils = get_sigils(card_1, card_2)

            # confirm the merge (visually show the cards being combined as an addition equation)
            confirm, result = confirm_choice(card_1, card_2, result_sigils)
            if not confirm :
                continue

            # add the new card to the deck
            campaign.add_card(result)

            # remove the merged cards from the deck
            campaign.remove_card(card_1)
            campaign.remove_card(card_2)

            break

    gameplay(campaign) # add flavor text, context, etc.

def pelt_shop(campaign) : # format visuals
    '''
    allow the player to buy pelts from the trapper with teeth

    one free rabbit pelt is given, and costs increase with current area/level

    costs permanently decrease after trapper boss fight has been beaten

    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    def display_shop(campaign, pelt_dict, new_pelts) :
        # set up variables
        card_gap_spaces = ' '*((os.get_terminal_size().columns*55 // 100) // 5 - 15)
        price_tags = QoL.center_justified(card_gap_spaces.join([f'{pelt_name.title()}: {str(pelt_dict[pelt_name][0]).ljust(13 - len(pelt_name))}' for pelt_name in pelt_dict]))
        pelt_displays = QoL.print_deck([pelt_dict[pelt_name][1] for pelt_name in pelt_dict], centered=True, blocked=True, fruitful=True)
        shop_display = f'{price_tags}{pelt_displays}'
        cart = QoL.print_deck(new_pelts, fruitful=True)

        # print the shop
        QoL.clear()
        print('\n')
        print(QoL.center_justified('You have ' + str(campaign.teeth) + ' teeth to spend') + '\n')
        print(shop_display)
        print(f'{card_gap_spaces}Cart:', end='')
        print(cart, end='')

    def buy_pelt(campaign, pelt_name, pelt_dict, new_pelts) :
        if campaign.teeth >= pelt_dict[pelt_name][0] :
            campaign.add_teeth(-pelt_dict[pelt_name][0])
            new_pelts.append(type(pelt_dict[pelt_name][1])())
        else :
            display_shop(campaign, pelt_dict, new_pelts)
            print('\n')
            input(QoL.center_justified(f'You do not have enough teeth to buy a {pelt_name.lower()} (press enter to go back)').rstrip() + ' ')

    def gameplay(campaign, cost_modifier) :
        # set up variables
        pelt_dict = {
            'rabbit pelt': [QoL.bind_int((1 + cost_modifier), 1, 2), card_library.RabbitPelt()],
            'wolf pelt': [QoL.bind_int((2 + cost_modifier), 2, 6), card_library.WolfPelt()],
            'golden pelt': [QoL.bind_int((3 + cost_modifier), 3, 11), card_library.GoldenPelt()]
        }
        new_pelts = [card_library.RabbitPelt()] # give the player a free rabbit pelt
        invalid_choice = False

        while True :
            # display the shop
            display_shop(campaign, pelt_dict, new_pelts)

            # get user input
            options = '''
1. Buy a pelt
2. View deck
3. Leave the shop'''
            print(QoL.center_justified(options, blocked=True))

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                invalid_choice = False
            else :
                print('\n')

            # get the user's choice
            choice = input(QoL.center_justified(' '*2 + 'Choose an option:').rstrip() + ' ')
            
            match choice :
                case '1' :
                    # display the shop
                    display_shop(campaign, pelt_dict, new_pelts)
                    print()
                    match input(QoL.center_justified('Would you like to buy 1) a Rabbit Pelt, 2) a Wolf Pelt, or 3) a Golden Pelt? (press enter to go back)').rstrip() + ' ') :
                        case '1' : 
                            buy_pelt(campaign, 'rabbit pelt', pelt_dict, new_pelts)
                        case '2' :
                            buy_pelt(campaign, 'wolf pelt', pelt_dict, new_pelts)
                        case '3' :
                            buy_pelt(campaign, 'golden pelt', pelt_dict, new_pelts)
                        case _ : 
                            invalid_choice = True
                case '2' :
                    # print the player's deck
                    QoL.clear()
                    print('\n'*5)
                    print(QoL.center_justified('Your deck:'))
                    campaign.print_deck()
                    print()
                    input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')
                case '3' : break
                case _ : invalid_choice = True

        # add pelts to the player's deck
        for pelt in new_pelts :
            campaign.add_card(pelt)

    [beat_trapper] = QoL.read_data([['progress markers', 'beat trapper']])
    cost_modifier = 0 + campaign.level - beat_trapper

    gameplay(campaign, cost_modifier) # add flavor text, context, etc.

def card_shop(campaign) : # format visuals
    '''
    allow the player to buy cards from the trader with pelts from their deck

    arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    # set up functions
    same_sigil = lambda sigil_1, sigil_2 : sigil_1 != '' and (sigil_1 == sigil_2 or all('lane shift' in sigil for sigil in [sigil_1, sigil_2]) or all('hefty' in sigil for sigil in [sigil_1, sigil_2])) 

    def add_sigil_wolf(card_) :
        allowed_sigils = [sigil for sigil in sigils.Dict if not any(same_sigil(sigil, sigil_) for sigil_ in card_.sigils)]
        sigil_slot = card_.sigils.index('')
        card_.sigils[sigil_slot] = random.choice(allowed_sigils)
        card_.update_ASCII()
        return card_
    
    def pelt_trade(campaign, pelt, available_cards) : 
        '''
        allows the player to trade a pelt for a card

        arguments:
            campaign: the current campaign object (rogue_campaign object)
            pelt: the pelt to trade (card object)
            available_cards: the cards available for trade (list[card object])

        returns:
            bool: True if the trade is successful, False if it is not
        '''
        # set up variables
        invalid_choice = False

        while True :
            # display the trade options
            QoL.clear()
            print('\n'*3)
            QoL.print_deck([pelt])
            print()
            QoL.print_deck(available_cards, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                invalid_choice = False
            else :
                print('\n')

            # get user input
            match input(QoL.center_justified(f'Which card will you trade your {pelt.species.lower()} for? (press enter to go back)').rstrip() + ' ').lower() :
                case index if QoL.reps_int(index)[0] and int(index) - 1 in range(len(available_cards)) : # trade the pelt for the card
                    campaign.add_card(available_cards[int(index) - 1])
                    campaign.remove_card(pelt)
                    available_cards.remove(available_cards[int(index) - 1])
                    return True
                case '' : return False
                case _ : invalid_choice = True

    def random_card(possible_cards, alpha=2.2, beta=3.3, rare=False, open_sigil=False) :
        import math

        # get card
        if rare :
            template_card = random.choice(possible_cards)
            card_class = type(template_card)
        else :
            # get cost
            max_cost = max(possible_cards.keys())
            cost = math.floor((max_cost + 1) * random.betavariate(alpha, beta))

            while True :
                template_card = random.choice(possible_cards[cost])
                card_class = type(template_card)
                if not any(type(card) == card_class for card in card_library.Rare_Cards) and not (open_sigil and not template_card.has_sigil('')): break

        return card_class(getattr(template_card, 'blank_cost', False))

    def gameplay(campaign) :
        # set up variables
        invalid_choice = False
        pelt_order = lambda pelt : ['rabbit pelt', 'wolf pelt', 'golden pelt'].index(pelt.species.lower())
        deck_pelts = [card_ for card_ in campaign.player_deck.cards if 'pelt' in card_.species.lower()]
        deck_pelts.sort(key=pelt_order)
        rabbit_available = [random_card(card_library.Poss_Playr) for _ in range(8)]
        wolf_available = [add_sigil_wolf(random_card(card_library.Poss_Playr, open_sigil=True)) for _ in range(8)]
        golden_available = [random_card(card_library.Rare_Cards, rare=True) for _ in range(4)]

        while True :
            # player picks which pelt to trade (select from a filtered deck)
            if not deck_pelts :
                return
            QoL.clear()
            print('\n'*5)
            print(QoL.center_justified('Your pelts:'))
            QoL.print_deck(deck_pelts, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                invalid_choice = False
            else :
                print('\n')

            # get user input
            match input(QoL.center_justified('Which pelt will you trade for cards? (press enter to go back)').rstrip() + ' ') :
                case index if QoL.reps_int(index)[0] and int(index) - 1 in range(len(deck_pelts)) : # trade the pelt
                    pelt = deck_pelts[int(index) - 1]
                    match pelt.species.lower() :
                        case 'rabbit pelt' if pelt_trade(campaign, pelt, rabbit_available) : deck_pelts.remove(pelt)
                        case 'wolf pelt' if pelt_trade(campaign, pelt, wolf_available) : deck_pelts.remove(pelt)
                        case 'golden pelt' if pelt_trade(campaign, pelt, golden_available) : deck_pelts.remove(pelt)
                case '' : return
                case _ : invalid_choice = True
    
    # if player has no pelts in their deck, give them 5 teeth
    if not any(type(card_) in [card_library.RabbitPelt, card_library.WolfPelt, card_library.GoldenPelt] for card_ in campaign.player_deck.cards) :
        ### dialogue from trader on player's lack of pelts
        campaign.add_teeth(5)
    else :
        gameplay(campaign) # add flavor text, context, etc.

def break_rocks(campaign) : # format visuals
    '''
    allows the player to break one of three rocks to receive a bug card or (rarely) a golden pelt (prospector event)
    
    bugs may have additional sigils
    
    only one rock has a golden pelt
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    # set up variables for functions
    number_sprites = {
        1 : [' , ','/| ',' | ','‾‾‾'],
        2 : ['/‾\\','  /',' / ',' ‾‾'],
        3 : ['/‾\\',' _/',' ‾\\','\_/']
    }
    rock_sprites = {
        'chunky' : r'''
           __________
       ___/          \
     _/               \
    /         {0}      \___
 __/          {1}          \
/             {2}           |
\             {3}           |
 \                         /
  \_______________________/
''',
        'spiky' : r'''
           _
          / \    _
    _    /   \__/ \
   / \__/      /   \
  /     \      \    \  _
 /      /\  {0}      \/ \
|        /  {1}      /   \
|           {2}           |
|           {3}           |
 \_______________________/
''',
        'round' : r'''
            ___________
       ____/           \____
    __/                     \__
  _/                           \_
 /              {0}              \
|               {1}               |
|               {2}               |
 \_             {3}             _/
   \__                       __/
      \_____________________/
''',
    }
    broken_rock_sprites = {
        'chunky' : [
            r'''
           ___
       ___/   \
     _/        \
    /         {0[0]}/
 __/          {1[0]}\
/             {2[0]}/
\             /
 \           /
  \__________\
''',
            r'''
 _______
 \      \
  \      \
  /{0[1]}      \___
  \{1[1]}          \
  /{2[1]}           |
 /{3[1]}{3[2]}           |
/             /
\____________/
'''
        ],
        'spiky' : [
            r'''
           _
          / \
    _    /   \
   / \__/     \
  /     \     /
 /      /\  {0[0]}/
|        /  {1[0]}\
|           {2[0]}{2[1]}\
|           {3[0]}{3[1]}/
 \____________\
''',
            r'''

    _
 __/ \
 \/   \
 /\    \  _
/{0[2]}      \/ \
\{1[2]}      /   \
 \           |
 /           |
 \__________/
 '''
        ],
        'round' : [
            r'''
            ______
       ____/     /
    __/          \
  _/             /
 /              {0[0]}\
|               {1[0]}/
|               {2[0]}\
 \_             {3[0]}/
   \__           \
      \__________/
''',
            r'''
 _____
/     \____
\          \__
/             \_
\{0[2]}              \
/{1[2]}               |
\{2[2]}               |
/{3[2]}             _/
\           __/
/__________/
'''
        ],
    }

    def display_rocks(displayed_rocks) :
        '''
        display the available rocks to break to the player
        
        Arguments:
            displayed_rocks: the rocks to display (list[key(str), key(str), key(str)])
        '''
        # at least 5 different rock sprites that can be numbered with string formatting

        # set up functions
        longest_line = lambda lines: max([len(line) for line in lines])
        regular_width = lambda line, width: line + (width - len(line))*' '

        # insert numbers into the rock sprites
        numbered_rocks = [rock_sprites[displayed_rocks[ind]].format(*number_sprites[ind+1]) for ind in range(3)]

        # separate sprites into lines
        rock_lines = [rock.split('\n')[1:-1] for rock in numbered_rocks]

        # make sure the 2nd and 3rd rocks are the same height
        if len(rock_lines[1]) < len(rock_lines[2]) :
            rock_lines[1] = ['']*(len(rock_lines[2]) - len(rock_lines[1])) + rock_lines[1]
        elif len(rock_lines[2]) < len(rock_lines[1]) :
            rock_lines[2] = ['']*(len(rock_lines[1]) - len(rock_lines[2])) + rock_lines[2]

        # get the width of each rock
        rock_widths = [longest_line(rock_lines[ind]) for ind in range(3)]

        # combine the 2nd and 3rd rocks into one string
        rocks_2_3 = '\n'.join([regular_width(rock_lines[1][ind], rock_widths[1]) + (rock_widths[0] // 2)*' ' + regular_width(rock_lines[2][ind], rock_widths[2]) for ind in range(len(rock_lines[1]))])

        rocks_str = QoL.center_justified(numbered_rocks[0], True) + QoL.center_justified(rocks_2_3,True)

        print(rocks_str)
    
    def display_reward(selected, number, reward) :
        '''
        display the selected rock (broken in half) and the reward received

        Arguments:
            selected: the rock selected (str)
            number: the number of the rock selected (int)
            reward: the reward received (card object)
        '''
        # set up functions
        longest_line = lambda lines: max([len(line) for line in lines])

        # set up variables
        line_difference = 13 - len(broken_rock_sprites[selected][0].split('\n'))
        y_offset = line_difference // 2
        index_offset = line_difference - y_offset
        add_rock_lines = [False]*index_offset + [True]*(len(broken_rock_sprites[selected][0].split('\n')) - 2) + [False]*y_offset
        half_rock_width = max(longest_line(broken_rock_sprites[selected][0].format(*number_sprites[number]).split('\n')), longest_line(broken_rock_sprites[selected][1].format(*number_sprites[number]).split('\n')))

        # combine the rock halves and the reward into one string
        final_str = ''
        for ind in range(11) :
            left_rock_line = broken_rock_sprites[selected][0].format(*number_sprites[number]).split('\n')[ind - index_offset + 1]
            left_rock_line += ' '*(half_rock_width - len(left_rock_line))
            right_rock_line = broken_rock_sprites[selected][1].format(*number_sprites[number]).split('\n')[ind - index_offset + 1]
            right_rock_line += ' '*(half_rock_width - len(right_rock_line))
            reward_line = reward.text_lines[ind + 1]
            if add_rock_lines[ind] :
                final_str += left_rock_line
                final_str += ' '*7
                final_str += reward_line
                final_str += ' '*7
                final_str += right_rock_line
                final_str += '\n'
            else :
                final_str += reward_line
                final_str += '\n'

        print(QoL.center_justified(final_str))

    def random_insect() :
        chosen_card = random.choice(card_library.Insects)
        card_class = type(chosen_card)
        if any(type(card_) == card_class for card_ in card_library.Rare_Cards) :
            chosen_card = random.choice(card_library.Insects)
            card_class = type(chosen_card)
        
        return card_class(getattr(chosen_card, 'blank_cost', False))

    def gameplay(campaign) :
        # randomly select 3 insect cards
        available_rocks = random.sample(list(rock_sprites.keys()), 3)
        hidden_rewards = {
            0: random_insect(),
            1: random_insect(),
            2: random_insect()
        }

        # give sigils to the hidden rewards
        for hidden_reward in hidden_rewards.values() :
            if random.randint(1, 100) <= 50 and hidden_reward.has_sigil('') :

                same_sigil = lambda sigil_1, sigil_2 : sigil_1 != '' and (sigil_1 == sigil_2 or all('lane shift' in sigil for sigil in [sigil_1, sigil_2]) or all('hefty' in sigil for sigil in [sigil_1, sigil_2])) # check if two sigils are the same or variations of the same sigil
                good_sigil = lambda reciever, sigil : sigil != '' and not same_sigil(reciever.sigils[0], sigil) and not same_sigil(reciever.sigils[1], sigil) and sigil != '???' # check if a sigil can be added

                selected_sigil = ''

                while not good_sigil(hidden_reward, selected_sigil) : selected_sigil = random.choice(list(sigils.Dict.keys()))

                sigil_slot = hidden_reward.sigils.index('')

                hidden_reward.sigils[sigil_slot] = selected_sigil
                hidden_reward.update_ASCII()

        # one of the rewards is a golden pelt
        hidden_rewards[random.randrange(3)] = card_library.GoldenPelt()

        # set up variables
        invalid_choice = False

        while True :
            # print the available cards and options
            QoL.clear()
            print('\n'*5)
            display_rocks(available_rocks)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice') + '\n')
                invalid_choice = False
            else :
                print('\n')

            # get the user's choice
            match input(QoL.center_justified(' '*2 + 'Choose an option:').rstrip() + ' ') :
                case index if QoL.reps_int(index)[0] and int(index) - 1 in range(3) : # break the rock
                    # show the reward
                    QoL.clear()
                    print('\n'*5)
                    display_reward(available_rocks[int(index) - 1], int(index), hidden_rewards[int(index) - 1])

                    campaign.add_card(hidden_rewards[int(index) - 1])
                    
                    # wait for input before ending event
                    input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

                    return
                
                case _ : invalid_choice = True

    gameplay(campaign) # add flavor text, context, etc.

def campfire(campaign) : # format visuals
    '''
    each time a card rests by the Campfire, it gains a buff to its Power(+1) or Health(+2) (the stat is set before the player 'arrives')

    prior to 5 runs, the player can buff only once

    a card can be buffed up to 4 times per event, with the following chances of destruction:
    1 buff: 0% chance of destruction
    2 buffs: 22.5% chance of destruction
    3 buffs: 45% chance of destruction
    4 buffs: 67.5% chance of destruction
    '''
    def get_buffee(deck_list) :
        '''
        allows the player to choose a card to buff
        
        Arguments:
            deck_list: the list of cards to choose from (list[card object])
        
        Returns:
            card object: the card to buff
        '''
        # set up variables
        invalid_choice = False
        sorted_deck = QoL.sort_deck(deck_list)

        while True :
            # print the player's deck
            QoL.clear()
            QoL.print_deck(sorted_deck, numbered=True, centered=True, blocked=True)

            if invalid_choice :
                print(QoL.center_justified('Invalid choice'))
                print()
                invalid_choice = False

            # get user input
            card_index = input(QoL.center_justified('Enter the number of the card to buff:').rstrip() + ' ')

            (is_int, card_index) = QoL.reps_int(card_index, -1)

            if not is_int or card_index not in range(len(sorted_deck)) :
                invalid_choice = True
                continue

            return sorted_deck[card_index]
        
    def buff_card(card, stat) :
        '''
        buff a card's stat

        Arguments:
            card: the card to buff (card object)
            stat: the stat to buff (str)
        '''
        match stat :
            case 'attack' : card.base_attack += 1
            case 'life' : card.base_life += 2

        card.reset_stats()

    def eaten_card(card, campaign) :
        '''
        destroy a card

        Arguments:
            card: the card to destroy (card object)
            campaign: the current campaign object (rogue_campaign object)
        '''
        campaign.remove_card(card)
        QoL.clear()
        print('\n'*5)
        print(QoL.center_justified(f'{card.species} has been eaten by the survivors'))
        if card.species in ['Adder'] :
            campaign.dead_campfire = True
            print(QoL.center_justified('The survivors are now sick'))
        
    def gameplay(campaign) :
        # set up variables
        stat = random.choice(['attack', 'life'])
        [wins, losses] = QoL.read_data([['progress markers', 'wins'], ['progress markers', 'losses']])
        total_runs = wins + losses
        eat_chances = {
            1 : 0,
            2 : 225,
            3 : 450,
            4 : 675
        }
        not_eaten = lambda buff_number, campaign : campaign.dead_campfire or random.randint(1, 1000) > eat_chances[buff_number]

        # get the player's choice of card to buff
        card_choice = get_buffee(campaign.player_deck.cards)

        # first buff
        buff_card(card_choice, stat)

        # display the buffed card
        QoL.clear()
        print('\n'*5)
        card_choice.explain()

        # end if prior to 5 runs
        if total_runs < 5 :
            input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
            return

        # second to fourth buffs
        number_of_buffs = 1

        while number_of_buffs < 4 :
            # check if player wants to buff the card again
            QoL.clear()
            print('\n'*5)
            card_choice.explain()
            print('\n')
            if input(QoL.center_justified('Would you like to buff this card again? (y/n)').rstrip() + ' ').lower() != 'y' :
                break

            # increase the number of buffs
            number_of_buffs += 1

            # buff the card
            if not_eaten(number_of_buffs, campaign) :
                buff_card(card_choice, stat)
            else :
                eaten_card(card_choice, campaign)
                input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')
                return

    gameplay(campaign) # add flavor text, context, etc.

def add_death_card(campaign) : # format visuals
    '''
    allow the player to add a death card to the card pool
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''

    # making a death card will shift the values of 'second' to 'third', 'first' to 'second', and the new death card will be written to 'first'
    # flavoring should not mention it being a death card vs a victory card, as that will be handled in lost_run() and beat_leshy()

    def rotate_cards() :
        '''
        rotate the cards in the config file to empty the first slot and shift the others up
        
        Arguments:
            campaign: the current campaign object (rogue_campaign object)
        '''
        # set up variables
        data_to_read = [
            ['death cards', 'first', 'name'],
            ['death cards', 'first', 'attack'],
            ['death cards', 'first', 'life'],
            ['death cards', 'first', 'cost'],
            ['death cards', 'first', 'sigils'],
            ['death cards', 'first', 'easter'],
            ['death cards', 'second', 'name'],
            ['death cards', 'second', 'attack'],
            ['death cards', 'second', 'life'],
            ['death cards', 'second', 'cost'],
            ['death cards', 'second', 'sigils'],
            ['death cards', 'second', 'easter']
        ]
        [name_1, attack_1, life_1, cost_1, sigils_1, easter_1, name_2, attack_2, life_2, cost_2, sigils_2, easter_2] = QoL.read_data(data_to_read)
        data_to_write = [
            (['death cards', 'first', 'name'], None),
            (['death cards', 'first', 'attack'], None),
            (['death cards', 'first', 'life'], None),
            (['death cards', 'first', 'cost'], None),
            (['death cards', 'first', 'sigils'], None),
            (['death cards', 'first', 'easter'], None),
            (['death cards', 'second', 'name'], name_1),
            (['death cards', 'second', 'attack'], attack_1),
            (['death cards', 'second', 'life'], life_1),
            (['death cards', 'second', 'cost'], cost_1),
            (['death cards', 'second', 'sigils'], sigils_1),
            (['death cards', 'second', 'easter'], easter_1),
            (['death cards', 'third', 'name'], name_2),
            (['death cards', 'third', 'attack'], attack_2),
            (['death cards', 'third', 'life'], life_2),
            (['death cards', 'third', 'cost'], cost_2),
            (['death cards', 'third', 'sigils'], sigils_2),
            (['death cards', 'third', 'easter'], easter_2)
        ]
        QoL.write_data(data_to_write)

    def choose_card(dialogue, used_cards, campaign) :
        '''
        allow the player to choose a card from a list of three
        
        Arguments:
            dialogue: the dialogue to display (str)
            used_cards: the cards that have already been used (list[card object])
            campaign: the current campaign object (rogue_campaign object)
            
        Returns:
            card object: the card chosen
        '''
        # set up variables
        invalid_choice = False
        options = '''
1. View a card
2. Pick a card

'''
        card_pool = [card_ for card_ in campaign.player_deck.cards if not any(type(card_) == type(card__) for card__ in card_library.Poss_Death + used_cards)]
        option_cards = random.sample(card_pool, k=min(3, len(card_pool)))
        used_cards += option_cards

        # set up functions
        def print_top() :
            QoL.clear()
            print('\n'*5)
            print(QoL.center_justified(dialogue))
            QoL.print_deck(option_cards, numbered=True, centered=True)
            print(QoL.center_justified(options, blocked=True))

        while True :
            # print the available cards and options
            print_top()

            if invalid_choice :
                print(QoL.center_justified('Invalid choice') + '\n')
                invalid_choice = False
            else :
                print('\n')

            # get the user's choice
            choice = input(QoL.center_justified(' '*2 + 'Choose an option:').rstrip() + ' ')

            match choice :
                case '1' : # view a card
                    # print the available cards and options
                    print_top()

                    # get the user's choice
                    card_index = input(QoL.center_justified('Enter the number of the card to view:').rstrip() + ' ')
                    (is_int, card_index) = QoL.reps_int(card_index, -1)

                    if is_int and card_index in range(3) :
                        QoL.clear()
                        print('\n'*5)
                        print(QoL.center_justified(dialogue))
                        QoL.print_deck(option_cards, numbered=True, centered=True)
                        print()
                        option_cards[card_index].explain()
                        input(QoL.center_justified('Press Enter to go back...').rstrip() + ' ')
                    
                    else :
                        invalid_choice = True
                
                case '2' :
                    # print the available cards and options
                    print_top()

                    # get the user's choice
                    card_index = input(QoL.center_justified('Enter the number of the card to pick:').rstrip() + ' ')
                    (is_int, card_index) = QoL.reps_int(card_index, -1)

                    if is_int and card_index in range(3) :
                        return option_cards[card_index]
                    
                    else :
                        invalid_choice = True
                
                case _ :
                    invalid_choice = True

    def gameplay(campaign) :
        # set up variables
        used_cards = []
        cost_dialogue = 'Choose a card to take the cost from:'
        stat_dialogue = 'Choose a card to take the attack and life from:'
        sigil_dialogue = 'Choose a card to take the sigils from:'
        flavor_pic = '''
    After you finish your work, Leshy hands you a blank card and takes a picture. The last thing you remember is the flash of the camera and this card in your hand.
'''

        # get cost choice card
        cost_card = choose_card(cost_dialogue, used_cards, campaign)
        new_cost = cost_card.saccs

        # get stat choice card
        stat_card = choose_card(stat_dialogue, used_cards, campaign)
        new_attack = stat_card.base_attack
        new_life = stat_card.base_life

        # get sigil choice card
        sigil_card = choose_card(sigil_dialogue, used_cards, campaign)
        new_sigils = sigil_card.sigils

        # get the name of the death card
        QoL.clear()
        print('\n'*4)
        # show the WiP card with ??? for name
        WiP_card = card.BlankCard(species='???', attack=new_attack, life=new_life, cost=new_cost, sigils=new_sigils)
        QoL.print_deck([WiP_card], centered=True)
        print()
        new_name = input(QoL.center_justified('Enter the name of your new card:').rstrip() + ' ')

        # write the death card to config.json
        rotate_cards()

        data_to_write = [
            (['death cards', 'first', 'name'], new_name),
            (['death cards', 'first', 'attack'], new_attack),
            (['death cards', 'first', 'life'], new_life),
            (['death cards', 'first', 'cost'], new_cost),
            (['death cards', 'first', 'sigils'], new_sigils),
            (['death cards', 'first', 'easter'], False)
        ]
        QoL.write_data(data_to_write)

        # show the player the death card
        new_card = card_library.PlyrDeathCard1()
        QoL.clear()
        print('\n'*5)
        print(flavor_pic)
        print(QoL.center_justified('Your new card:'), end='')
        QoL.print_deck([new_card], centered=True)

        # wait for input before ending event
        input(QoL.center_justified('Press Enter to continue...').rstrip() + ' ')

    gameplay(campaign) # add flavor text, context, etc.

def lost_run(campaign) : # format visuals
    def gameplay(campaign) :
        # manage save data
        [losses] = QoL.read_data([['progress markers', 'losses']])
        QoL.write_data([(['progress markers', 'losses'], losses + 1)])

        if losses + 1 >= 4 :
            add_death_card(campaign)

        # visuals
        QoL.clear()
        ASCII_text.print_lose()

        # wait for input before ending run (which returns the player to the main menu)
        input(QoL.center_justified('Press Enter to return to the main menu...').rstrip() + ' ')

    gameplay(campaign) # add flavor text, context, etc.

def beat_leshy(campaign) : # format visuals
    def gameplay() :
        # manage save data
        [wins] = QoL.read_data([['progress markers', 'wins']])
        QoL.write_data([(['progress markers', 'wins'], wins + 1)])

        add_death_card(campaign)

        # visuals
        QoL.clear()
        ASCII_text.print_win()

        # wait for input before ending run (which returns the player to the main menu)
        input(QoL.center_justified('Press Enter to return to the main menu...').rstrip() + ' ')

    gameplay() # add flavor text, context, etc.

def split_road(campaign) : # format visuals
    '''
    presents the player with a choice from 1-3 paths, each with a different event, which will be known to the player before they choose
    
    Arguments:
        campaign: the current campaign object (rogue_campaign object)
    '''
    def get_event(campaign, previous_events=[]) :
        '''
        generate an event for a path according to weights
        
        could change weights depending on campaign level, etc.

        Arguments:
            campaign: the current campaign object (rogue_campaign object)
            previous_events: the events that have already been generated (list[int])
        
        Returns:
            list[str, str, int]: the event to run, the function to run it, and the number of the event
        '''
        # set up functions
        bool_to_bin = lambda bool_, int_=1 : int_ if bool_ else 0

        # set up variables
        weights = [
            bool_to_bin(1 not in previous_events), # card choice
            bool_to_bin(2 not in previous_events and len(campaign.player_deck.cards) > 4), # sigil sacrifice
            bool_to_bin(any(type(card_1) == type(card_2) and card_1 != card_2 for card_1 in campaign.player_deck.cards for card_2 in campaign.player_deck.cards) and 3 not in previous_events and len(campaign.player_deck.cards) > 4), # merge cards
            bool_to_bin(4 not in previous_events), # pelt shop
            bool_to_bin(any(type(card_) in [card_library.WolfPelt, card_library.RabbitPelt, card_library.GoldenPelt] for card_ in campaign.player_deck.cards) and 5 not in previous_events), # card shop
            bool_to_bin(6 not in previous_events), # break rocks
            bool_to_bin(7 not in previous_events), # campfire
            bool_to_bin(8 not in previous_events, 2 and len(campaign.player_deck.cards) > 3) # card battle
        ]

        match random.choices(range(1, 9), weights=weights)[0] :
            case 1 : return ['A choice of cards', 'card_choice(campaign)', 1]
            case 2 : return ['A set of mysterious stones', 'sigil_sacrifice(campaign)', 2]
            case 3 : return ['The Mycologists', 'merge_cards(campaign)', 3]
            case 4 : return ['The Trapper', 'pelt_shop(campaign)', 4]
            case 5 : return ['The Trader', 'card_shop(campaign)', 5]
            case 6 : return ['The Prospector', 'break_rocks(campaign)', 6]
            case 7 : return ['Survivors huddled around a campfire', 'campfire(campaign)', 7]
            case 8 : return ['A card battle', 'card_battle(campaign)', 8]

    def gameplay(campaign) :
        # set up variables
        term_cols = os.get_terminal_size().columns
        card_gap = ((term_cols*55 // 100) // 5 - 15) * ' '

        # get the paths
        ## 50% chance for two paths, 25% for one and three
        match random.randint(1, 4) :
            case 1 : # one path
                path_list = [get_event(campaign)]
            case 2 : # three paths
                # path_list = [get_event(campaign), get_event(campaign), get_event(campaign)]
                path_list = [get_event(campaign)]
                previous_events = [path_list[0][2]]
                path_list.append(get_event(campaign, previous_events))
                previous_events.append(path_list[1][2])
                path_list.append(get_event(campaign, previous_events))
            case _ : # two paths
                path_list = [get_event(campaign)]
                previous_events = [path_list[0][2]]
                path_list.append(get_event(campaign, previous_events))

        invalid_choice = False
        while True :

            # display the paths
            QoL.clear()
            print('\n'*5)
            for ind in range(len(path_list)) : print(f'{card_gap}Path {str(ind + 1)}: {path_list[ind][0]}')

            if invalid_choice :
                print(QoL.center_justified('Invalid choice') + '\n')
                invalid_choice = False
            else :
                print('\n')

            # get the player's choice
            match QoL.reps_int(input(QoL.center_justified('Which path will you take?').rstrip() + ' '), -1) :
                case [False, _] : invalid_choice = True
                case [True, choice] : return exec(path_list[choice][1], globals(), locals())
        
    gameplay(campaign) # add flavor text, context, etc.

def main() : # coordinates the game loop, calls split_road, manages losses, initiates the game, etc.

    # after the player has won a run, start with three lives
    if QoL.read_data([['progress markers', 'wins']])[0] > 0 : life_count = 3
    else : life_count = 2

    # create starting deck list (switch rabbit for opossum once bones are implemented)
    starting_deck = [card_library.Wolf(), card_library.Stoat(), card_library.Bullfrog(), card_library.Rabbit()]

    # initialize campaign object
    campaign = rogue_campaign(starting_deck, lives=life_count)

    # dialogue, flavor text, etc.

    # loop is:
    while True :
            # ping variables
            ping_vars={}
            ping_vars['campaign level'] = campaign.level
            ping_vars['campaign progress'] = campaign.progress
            ping_vars['campaign lives'] = campaign.lives
            ping_vars['campaign teeth'] = campaign.teeth
            ping_vars['campaign player deck'] = campaign.player_deck.cards
            ping_vars['campaign squirrel deck'] = campaign.squirrel_deck.cards
            ping_vars['campaign dead campfire'] = campaign.dead_campfire
            for card_ in campaign.player_deck.cards :
                ping_vars[f'campaign player deck {card_.species}'] = {
                    'attack' : card_.base_attack,
                    'life' : card_.base_life,
                    'cost' : card_.saccs,
                    'sigils' : card_.sigils
                }
            QoL.ping(ping_vars)


    ###     check if area boss is next event (campaign.progress >= 10)
            if campaign.progress >= 10 :
    ###         if it is, and its Leshy (campaign.level == 3), check if player has won
                if campaign.level == 3 and bosses.boss_fight_leshy(campaign) :
    ###             if they have, run beat_leshy, and return (to main menu)
                    beat_leshy(campaign)
                    return
    ###         if it is, run boss event according to the current level and check if player has won
                elif (campaign.level == 0 and bosses.boss_fight_prospector(campaign)) or (campaign.level == 1 and bosses.boss_fight_angler(campaign)) or (campaign.level == 2 and bosses.boss_fight_trapper_trader(campaign)) :
    ###             if they have, update the level, reset the progress, and print flavor text for the new area
                    campaign.level += 1
                    campaign.progress = 0
                    print(f'You have reached the {campaign.level}th area')
                    print()
                    input('Press Enter to continue...')
    ###     else, run split_road
            else : 
                # playtest feature to quick quit
                import sys
                QoL.clear()
                print('\n'*5)
                if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')) :
                    quit_game = input('(PLAYTEST FEATURE) Quit game? (y/n) ')
                    if quit_game == 'y' :
                        return
                split_road(campaign)
    ###     check campagin.has_lost
            if campaign.has_lost() :
    ###         if True, run lost_run, and return (to main menu)
                lost_run(campaign)
                return
    ###         else, increment campaign.progress and continue loop
            else :
                campaign.progress += 1
                campaign.player_deck.refresh_ASCII()

if __name__ == '__main__' :
    pass