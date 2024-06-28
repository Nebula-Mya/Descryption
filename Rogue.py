# this file will handle the rogue-like gameplay, such as random encounters, random events, bosses, etc.

### classes

# campaign, which stores the current campaign data, such as the current level, the current decks, teeth (money), progress in the level, etc.

### functions: (more to be added later, these are just the most important to add)

# random encounter

# get card (choose from 3 cards taken from card_library.Poss_Playr or pelts)

# sacrifice card for sigil

# pelt shop (trapper)

# death / loss (create death card)

# win (create 'win' card, largely the same as death / loss function, differing mostly in flavor)

##### bosses will use the basic AI, but with higher difficulty settings and have their unique mechanics (pickaxe, ship, moon)

# boss fight 1 (the miner) 

# boss fight 2 (the pirate)

# boss fight 3 (Leshy)

# split_road (choose path, the main function that handles all others, most of the game loop will be here)

# main (coordinates the game loop, calls split_road, manages losses, initiates the game, etc.)