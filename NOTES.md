# Notes
> sort field objects by zone  
>
> cards attack from left to right
>
> after cards attack, check if card.status == 'dead', if so, call card.die() (for sigils) and move it to graveyard object
>
>> BEFORE MOVING TO GRAVEYARD, check if card.status == 'undead', if so, move it to the hand
>>
>> also replace it with a blank card with same zone  
>>
>> when playing a card, delete the current blank card in that zone, call card.play(zone), and move it to the field object
>> 
> field object should use a dictionary, with keys being zones  
>
>> maybe one field object with sub dictionaries for rows?  
>>
>> on turn end, re order the field according to zones
>> 
> graveyard should be viewable to player 
>
>> should be a list for ordering 
>
> at beginning of turn, check if decklist length + squirrel length is <= 0, if so, player loses
>
> slime mold sigil is names 'split'
>
> need extra blank cards on the sides to prevent crashes, they wont get drawn (zones 0 and 6)
>
> when sacrificing, call card.sacc() and move it to graveyard, replacing it with a blank card with same zone
>
> Leshy card advancing ideas:
>> go through leshy's field, and when a zone is empty, replace it with the same zone from the bushes (this will replace blanks with blanks, thats important)
>>
>> instead of just replacing the now empty bush zone with a blank card, randomly assign it one of the cards or to be blank (weighted, will require balancing)
>>
>> the weighting could be impacted by gamestate for very basic ai (ie, decrease odds of blank if the player has a card in the same column)
>>
>> which card is chosen is based on Leshy's decklist, which is randomly generated with more weaker cards and fewer strong cards, and is twice the size of the player's + 20 so as to prevent Leshy from running out of cards easily
>
> when playing card:
>> select card to play with index in hand (starting with 1)
>> 
>> focus on selected card in hand (card.explain()), replacing hand
>>> can unselect card with 0
>>>
>>> can select saccs with zone numbers (1-5)
>>>> if an empty zone is selected, nothing changes and menu loops
>>>
>>> sacc menu loops until enough saccs are chosen
>>>
>>> displays a list of selected saccs in format 'card(zone)' (ie 'Sacrifices: squirrel(1), wolf(4)')

## Path from /root
/mnt/c/Users/MaWmM/Documents/GitHub/final-project-Nebula-Mya