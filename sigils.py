Dict = {
    '' : [ # sigil name
        ["     ","     ","     "], # sigil icon
        '' # sigil description
        ],

    'bifurcate' : [
        ["_   _"," \ / ","  |  "],
        'Attacks diagonally, dealing damage to two targets.'
        ],

    'lane shift right' : [
        [",-,  ","| |->","'-'  "], 
        'Moves right after attacking if possible.'
        ],

    'lane shift left' : [
        ["  ,-,","<-| |","  '-'"],
        'Moves left after attacking if possible.'
        ],

    'split' : [
        ["  |  ","()|()","  |  "],
        'Splits into two cards when killed.'
        ],

    'unkillable' : [
        [",->-,","| X |","'-<-'"],
        'Returns to hand on death.'
        ],

    'venom' : [
        [" ___ "," \\ / "," ·V· "],
        'Poisons target on attack.'
        ],

    'airborne' : [
        ["  _  ","ɩΞΞɭ "," ɩΞΞð"],
        'Attacks from the air, ignoring other creatures.'
        ],

    'mighty leap' : [
        ["_____","ʅ   ʃ"," ʅɩð "],
        'Can block airborne creatures.'
        ],

    'worthy sacrifice' : [
        ["(C)  "," (C) ","  (C)"],
        'Worth three sacrifices.'
        ],

    'bees within' : [
        [" /‾\\ ","|___|","  Ʈ->"],
        'Adds a bee to your hand when damaged.'
        ],

    'hefty (right)' : [ 
        [". >>>","|)_[]","'———'"],
        'Moves to the right, pushing other creatures with it.'
        ],
    
    'hefty (left)' : [
        ["<<< .","[]_(|","'———'"],
        'Moves to the left, pushing other creatures with it.'
        ],

    'many lives' : [ 
        ["  Ω  "," CXƆ ","  V  "],
        "Doesn't die when sacrificed."
        ],

    'waterborne' : [ # unimplemented
        ["<⁻v⁻>","ˎ\\ /ˏ","λ/λ\\λ"],
        'Attacks directed toward this card hit the owner directly.'
        ],
        # waterborne cards:
        ### ___

    'vole hole' : [ # unimplemented
        [" ___ ","/…¨…\\","‾‾‾‾‾"],
        'Adds a vole to your hand when played.' # vole is C0 0/1
        ],
        # vole hole cards:
        ### Warren (C1 0/2 Vole Hole) ['warren' can be used properly for animals other than rabbits, I checked]

    'touch of death' : [ # unimplemented
        ["\\´‾`/","|°Δ°|","/\'\"\'\\"],
        'Always kills the card it attacks, regardless of health.'
        ],
        # touch of death cards:
        ### ___

    'dam builder' : [ # unimplemented
        ["~~/\\ ","~/\\_\\","/__\\ "],
        'Builds dams on either side when played.' # dam is C0 0/2
        ],
        # dam builder cards:
        ### ___
}

if __name__ == '__main__':
    import card
    import QoL
    import os
    QoL.clear()
    term_cols = os.get_terminal_size().columns
    card_gaps = (term_cols*55 // 100) // 5 - 15
    tab = ' '*(card_gaps // 2)
    for key in Dict:
        if key == '':
            continue
        print(tab + QoL.title_case(key) + ':')
        example = card.BlankCard(sigil=key)
        example.species = 'EXAMPLE CARD'
        example.explain()
        print()