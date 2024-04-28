# Project Proposal
### Due: (Spring 2024) 11:59PM on Tuesday 4/30/2024

This file will contain your Final Project Proposal. Answer the prompts below to outline your project. If you are struggling to think of ideas, refer to the [Project Overview](https://cs.oberlin.edu/~cs150/final-project/part-1/) for suggestions.

### (1) What is the title of your project?
> Descryption

### (2) In 3-5 sentences, summarize what you want to accomplish. Provide enough detail so that I can understand your main idea, but try to keep things concise.
> Descyption is an MS-DOS text adventure style demake of the indie card game Inscryption. Ill be using modular ASCII art/graphics for most UI. Gameplay outside of card games will be solely text based. It will be played entirely through the terminal, with user interaction via command line inputs. 


### (3) Try "backwards-designing" from your main idea and draft your program overview. See previous labs and/or coding demos for examples.
1. Inputs: What will you request from the user?
> Gameplay commands, such as card selection from hand, zone selection, and option selection in text based segments. 

2. Computation: How are you transforming the inputs into something else? What data types could be helpful for managing information in the program? What functions will you create/use to produce specific effects?
> Inputs are taken using input() and will simply be used for if statements or class instance retrieval. Classes will be used heavily for card types, as well as limited use of text files for permanent and possibly semi-permanent data storage. 

3. Outputs: What will you present to the user?
> All interaction and gameplay is entirely through the terminal, using text based gameplay and ASCII art for UI and other graphics.


### (4) In a numbered list, briefly describe your intermediate goal(s) based on your program overview.
Note that you will reflect on how well you were able to meet your intermediate goal(s) in your Progress Report.
> 1. Design basic ASCII graphics (card outlines and the like)
> 2. Construct framework for card-based gameplay (opponent "AI" entirely random)
> 3. Add ASCII emblems for sigils
> 4. Impliment cards to allow for testing and balancing
> 5. Impliment light AI for opponent (only changing zone selection, card order stays random and predetermined)
> 6. Impliment rogue gameplay loop: add text based path choosing and game overs
> 7. Impliment difficulty increase and player power increase throughout a run (including pre-set first battle)
> 8. Balance balance balance


### (5) Are you strongly committed to this idea, or would you like suggestions for alternatives?
> I'm strongly committed.

