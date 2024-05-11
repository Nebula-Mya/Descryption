class Playmat :
    '''
    The field of play, including the bushes, the cards in play, the player's hand, and the score.

    Arguments:
        deck: the player's deck (list)
        opponent_deck: Leshy's deck (list)
    
    Other Attributes:
        bushes: the bushes on the field (dict)
        player_field: the cards in play (dict)
        opponent_field: Leshy's cards in play (dict)
        hand: the cards in the player's hand (list)
        graveyard: the cards in the graveyard (list)
        score: the score of the game (dict)
        active: the active player (str)

    Methods:
        draw() : draws a card from the deck to the hand
        play_card(index, zone) : plays a card to the field (first opens card explanation and has player select saccs, then plays card to zone)
        attack() : attacks with all cards in play
        check_states() : checks for dead cards and removes them
        advance() : advances cards from bushes to field
        switch() : switches the active player
        check_win() : checks for a win
        print_field() : prints the field
        print_full_field() : prints the field and player's hand
    '''