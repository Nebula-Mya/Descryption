# Path from /root
/mnt/c/Users/MaWmM/Documents/GitHub/final-project-Nebula-Mya

# notes
> sort field objects by zone  
>
> cards attack from left to right
>
> after cards attack, check if card.status == 'dead', if so, call card.die(zone) (for sigils) and move it to graveyard object
>
>> BEFORE MOVING TO GRAVEYARD, check if card.status == 'undead', if so, move it to the hand
>
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
> at beginning of turn, check if decklist length is <= 0, if so, player loses  
>
> slime mold sigil is names 'split'
>
> need extra blank cards on the sides to prevent crashes, they wont get drawn (zones 0 and 6)