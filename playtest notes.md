<!-- LTeX: enabled=false -->
# Playtest Notes

## Bugs:

- [x] check that cards aren't being added as same instance from library (need to make library stuff be lists of classes instead of instances - will be big change) (also change the creation of blankcards for copies to be of the right type, cause species checks are changing to type checks)
 > #### Files to revise:
 > - [x] card_library.py
 > - [x] QoL.py
 > - [x] bosses.py
 > - [x] card.py
 > - [x] deck.py
 > - [x] duel.py
 > - [x] field.py
 > - [x] menu.py
 > - [x] rogue.py
 > - [x] sigils.py

- [x] prevent it from adding mystery sigil (known to happen with trader)

- [x] fix grammar with trapper (1 teeth) (and with post boss screen)

- [x] dont let 0 costs be summoned on top of other cards...

- [x] get teeth from boss battles

- [x] dam builder should inherit sigils

- [x] increase ouro's stats on sacc

- [x] stop stones from appearing when no card has open slots (its a softlock)

- [x] make cost use hex and roll over, mycologists exists

- [ ] crashes before final boss. still. fucking god dammit i swear to fucking god.
Traceback (most recent call last):
  File "/mnt/c/Users/MaWmM/Documents/GitHub/Descryption/menu.py", line 404, in <module>
    main_menu()
  File "/mnt/c/Users/MaWmM/Documents/GitHub/Descryption/menu.py", line 383, in main_menu
    rogue.main()
  File "/mnt/c/Users/MaWmM/Documents/GitHub/Descryption/rogue.py", line 1750, in main
    if campaign.level == 3 and bosses.boss_fight_leshy(campaign) :
  File "/mnt/c/Users/MaWmM/Documents/GitHub/Descryption/bosses.py", line 1151, in boss_fight_leshy
    return gameplay(campaign)[1] == 'player' # add flavor text, context, etc.
  File "/mnt/c/Users/MaWmM/Documents/GitHub/Descryption/bosses.py", line 1111, in gameplay
    for cost in poss_leshy.keys() :
RuntimeError: dictionary changed size during iteration



## Improvements:

- [x] For mystery cards, dont show 0/0 stats for explanation (in card choice event)

- [x] be able to view deck when choosing path

- [x] show explanation after prospector event

- [x] clarify steel trap text (check if leshy is given a pelt??)

- [x] show card when drawing from resource too

- [x] display win results after boss

- [x] be able to see how many teeth you have

- [x] be able to check deck before choosing draw

- [ ] on very hard (or maybe also hard), start with cards on front row, also increase amount needed to win????

<!-- - [ ] maybe let survivors lower cost -->

<!-- - [ ] make it so stones can replace sigils -->

<!-- - [ ] maybe make unkillable not work on sacc (wait for further testing after bug fixes) -->

<!-- - [ ] maybe get rid of starting squirrel (give another main deck card, will need update to fair draw implementation) -->

<!-- - [ ] add another use for teeth (upgrade or remove cards? campfire cost?? REMOVE SIGILS!!) -->

<!-- - [ ] add insentive for bigger, messier decks (safety without softlock???????????) -->

<!-- - [ ] in sacrifice for sigils event, allow to go back at any point, not just end confirmation -->