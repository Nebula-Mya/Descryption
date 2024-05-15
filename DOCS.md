# Documentation
### Due: (Spring 2024 Final Exam Schedule)
* Section 1 (Professor Michael): 11AM on Thursday 5/16/2024
* Section 2 (Professor Noel): 9PM on Wednesday 5/15/2024
* Section 3 (Professor Michael): 9PM on Thursday 5/16/2024
* Section 4 (Professor Emily): 9PM on Wednesday 5/15/2024

This file will contain your project Documentation. Fill out the relevant sections to document your code.

## Summary
#### Briefly describe your program and what it does.
My program, "Descryption", is a console-based game featuring card-based gameplay. It is a demake of the indie game "Inscryption" made by Daniel Mullin meant to emulate the style of MS-DOS games. 

## Main File
#### What is the "main" file for your program, i.e. what should I run first?
"menu.py" is the main file to run. You can also use the binary executable included in the v0.1.2-alpha release, though the gui of the main menu is slightly older. 

## Example Usage
#### Provide examples of how the user should run your program.
It's designed as a stand-alone game, albeit not very complex yet. I suppose they should run it to play and enjoy it? The main file to run is responsible for the main menu and settings, as well as consolidating and managing all of the other files. So, uh, run menu.py and knock yourself out I suppose. 

## Input
#### Describe any input(s) required from the user.
Input is entirely done through the console, as it serves as the interface for the game. The user inputs selections to various menus to interact with the game, in a manner similar to how one would navigate menus in any other video game, albeit a bit more bare bones, which is intentional. 

## Output
#### Describe any output(s) produced by your program.
The main output is the graphics, which are created entirely via text and ASCII art on the console. The only other output is the changing of some .txt files which serve as permanent saves for certain settings and progress with a specific card. 

## Known Issues
#### Describe any known bugs, including workarounds to keep your program running.
The only thing I can think of is that I use extra card objects in my playmat class so as to avoid complicated interactions and edge cases with certain sigils, but there are no unresolved bugs that I know of. 

## References
#### List any external resources you used and a brief note about how/where you used them in your programs. For example: external modules not introduced previously in the course and sample images/audio used in your interactive system.
I used the itertools module for displaying the deck, graveyard, and hand. I used the copy module for the generation of decks. The title, win, and lose ASCII fonts were from https://www.asciiart.eu. The addition of Chunked to itertools for Python3.9 was from David Salvisberg on the python discussion boards. My binary executables were generated with pyinstaller via the GUI made by Brent Vollebregt on GitHub. My handling of .txt files changing location due to the conversion was based off of the documentation for cx_Freeze. And of course I based the entire project off of the wonderful game "Inscryption", created by Daniel Mullin. 

## Reminder
Don't forget you must also include an updated `README.md` and self-assessment with your final submission.
