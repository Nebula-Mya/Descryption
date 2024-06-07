def hefty_check(field, zone, direction) :
    '''
    recursively checks how many cards can be pushed by a card with hefty sigil

    Arguments:
        field: the field to check (dict)
        zone: the zone to check (int)
        direction: the direction to check (str)
    
    Returns:
        the number of cards that can be pushed, -1 being the card after the hefty one is open (int)
    '''
    # issue, will return positive values when it should return 0 because its just adding
    if direction == 'right' :
        if field[zone].species == '' : # only when the card after the card with hefty is empty
            return -1
        if field[zone+1].species != '' and zone < 5 :
            if hefty_check(field, zone+1, direction) == 0 :
                return 0
            return 1 + hefty_check(field, zone+1, direction)
        elif field[zone+1].species == '' and zone < 5 :
            return 1
        else :
            return 0
    elif direction == 'left' :
        if field[zone].species == '' : # only when the card after the card with hefty is empty
            return -1
        if field[zone-1].species != '' and zone > 1 :
            if hefty_check(field, zone-1, direction) == 0 :
                return 0
            return 1 + hefty_check(field, zone-1, direction)
        if field[zone-1].species == '' and zone > 1 :
            return 1
        else :
            return 0