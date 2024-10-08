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

- [ ] fix grammar with trapper (1 teeth) (and with post boss screen)

- [x] dont let 0 costs be summoned on top of other cards...

- [ ] get teeth from boss battles

- [x] dam builder should inheret sigils

- [x] increase ouro's stats on sacc



## Improvements:

- [x] For mystery cards, dont show 0/0 stats for explanation (in card choice event)

- [ ] in sacrifice for sigils event, allow to go back at any point, not just end confirmation

- [ ] implement saving current campaign in case of crashes

- [ ] be able to view deck when choosing path

- [ ] show explanation after prospector event

- [ ] clarify steel trap text (check if leshy is given a pelt??)

- [x] show card when drawing from resource too

- [ ] maybe let survivors lower cost

- [ ] display win results after boss

- [ ] be able to see how many teeth you have

- [ ] be able to check deck before choosing draw

- [ ] on very hard (or maybe also hard), start with cards on front row, also increase amount needed to win????

- [ ] make it so stones can replace sigils

- [ ] maybe make unkillable not work on sacc (wait for further testing after bug fixes)

- [ ] maybe get rid of starting squirrel (give another main deck card, will need update to fair draw implementation)