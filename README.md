[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=14894857)
# final-project
CSCI 150 Final Project

## Deadlines (Spring 2024)
* PROPOSAL.md Due: 11:59PM Tuesday 4/30/2024
* PROGRESS.md Due: 11:59PM Tuesday 5/7/2024
* Full Code, DOCS.md, & README.md Due: (Spring 2024 Final Exam Schedule)
  * Section 1 (Professor Michael): 11AM on Thursday 5/16/2024
  * Section 2 (Professor Noel): 9PM on Wednesday 5/15/2024
  * Section 3 (Professor Michael): 9PM on Thursday 5/16/2024
  * Section 4 (Professor Emily): 9PM on Wednesday 5/15/2024

## Self-assessment
### What bundle did you achieve, to the best of your knowledge?
I achieved all of bundle 4 except for submitting PROGRESS.md, which was due in part to medical complications. As such, I personally feel I achieved bundle 4. 

Please fill out the rubric below indicating which of the bundle requirements your project satisfies. Mark the checkboxes of the items you believe you have completed. When prompted, replace `<DATE>` with the appropriate dates, and `<FILE_NAME>` and `<LINE>` with the file name and line numbers of code where the requirement is fulfilled. (You are welcome to add more than one example if it makes sense to do so.) Be sure to update these so they are accurate for your current submission.

### Bundle 1 
* [X] The project is submitted by the deadline. Submitted On: `05/15/24` 
* [X] There is a clear effort to create an interactive system.
* [X] Your submission includes this *completed* ReadMe file describing how your project fulfills the requirements.
* [X] At least one of the Project Proposal, Progress Report, and Documentation was submitted by the deadline. 
  * Proposal Submitted On: `4/28/24` 
  * Progress Report Submitted On: `<DATE>` 
  * Documentation Submitted On: `05/15/24` 
* [X] Your interactive system contains the following components: 
    * [X] Variables and assignment. `duel.py`: `290` 
    * [X] Conditional statements (i.e., `if`/`elif`/`else`). `field.py`: `271` 
    * [X] Strings. `card.py`: `224` 
    * [X] Use of a module (either one you've written, or a built-in Python module like `math`). `menu.py`: `20`
    * [X] A `main()` function and `if __name__ == "__main__"`. `duel.py`: `334`

### Bundle 2
* [X] Your project meets all requirements for Bundle 1.
* [X] The program provides way to accept input from a user and produce output for them. `duel.py`: `11`
* [X] Your interactive system involves a nontrivial computation or transformation of user input.
    * Briefly describe: `My game uses inputs via the console to perform actions such as moving custom objects between custom data structures, conduct complex checks for damage and life which very depending on sigils, and editing txt files to augment game settings. `
* [X] Your interactive system demonstrates **four out of five** of the following features: 
    * [X] 1. Appropriate use of functions and/or class methods 
        * [X] At least one function includes a parameter (for methods: a parameter _in addition to_ `self`).`field.py`: `11`
        * [X] At least one function includes a `return` statement. `field`: `321`
        * [X] There are least two functions in addition to `main()`. `menu.py`: `33`, `menu.py`: `135`
    * [X] 2. Appropriate use of `for` and/or `while` loops. `field.py`: `166`
    * [X] 3. An application of explicitly nested loops:
        * [X] Your system must include at least one feature that makes use of a loop nested within another loop, all in the same function. `field.py`: `100`
        * [X] The nested loop should be used to accomplish a task needed for your project.
    * [X] 4. Appropriate use of a dictionary or a list of lists: 
        * [X] Start with an empty/blank instance of the data structure (e.g., `[]` or `{}`) and add data relevant to your application. `duel.py`: `278`
        * [X] Add/remove elements from it in your code. `duel.py`: `285` 
        * [X] Use the object to accomplish a task needed for your project. `duel.py`: `290`
    * [X] 5. Appropriate use of a user-defined class you wrote:
        * [X] Define a class. `field.py`: `38`
        * [X] Create at least one object using your class. `duel.py`: `297`
        * [X] Use the object to accomplish a task needed for your project. `duel.py`: `323`
* [X] Code contains comments and docstrings which explain the behavior of different system elements.
  * Filenames and line numbers of two examples: `card.py`: `92`, `duel.py`: `284`
* [X] Your code runs (even though it may produce some errors). `HELL YEAH IT RUNS!`
* [X] You completed two out of three of the Proposal, Progress Report, and Documentation, and submitted them by their respective deadlines (submission dates listed above).

### Bundle 3 
* [X] Your interactive system satisfies the criteria for Bundle 2 and also has the following characteristics: 
    * [X] The program handles incorrect user input elegantly (i.e., does not allow the program to continue if the user does not provide correct input, prints a message communicating why the input is incorrect, and allows the user to try again). `field.py`: `100`
    * [X] The code is divided into multiple files and functions according to good design principles.
        * [X] Minimum four total functions (`main()` plus three others)
          * Filename and line number where `main()` is defined: `duel.py`: `305`
          * Names of 3 other functions / methods: `card.takeDamage, field.advance, choose_and_play` 
    * [X] Conditional statements handle exclusive choice correctly (i.e. `elif` and `else` are properly used instead of a "waterfall" of separate `if` statements).
    * [X] Functions compute extensively on the complex data structure(s).
        * [X] Multiple functions have parameters and return statements.
          * Two names of functions / methods that satisfy this requirement: `winner_check, hefty_check`
        * [X] At least one function uses or modifies a nested list, dictionary or user-defined object. `duel.py`: `11`
        * [X] No global data structure(s) exist.
* [X] Your code runs without any meaningful errors.

### Bundle 4 
* [X] Your code is well-documented (for instance, each function includes a meaningful docstring).
* [X] Incorrect user input is handled using `try`/`except` where appropriate. `menu.py`: `72`
* [X] Your code is well-abstracted and extensible (for instance, your instructor could easily add a new feature or modify an existing one in the corresponding function definition).
* [ ] You submitted all three of the Proposal, Progress Report, and Documentation by their respective deadlines (submission dates listed above).
* [X] Your code runs without any errors whatsoever.
* [X] Your code goes above and beyond the requirements of the previous bundles.
  * Briefly describe relevant features and highlights: `I made a game!!! (I'm honestly very proud of myself) My entire project is based around handling user input elegantly and utilizing it in conjunction with custom classes (ie cards, decks, the field) and is able to display it all solely using custom ASCII art! In situations where I needed longer term data storage I figured out how to use text files to create permanent saves! I also learned how to compile all of it into a binary executable for Windows (I'd need to set up some VMs for other OSs and my linux subsystem is being buggy with pyinstaller) so that I could work with a friend of mine to playtest. Those releases are in the releases section of the repository. I'm also planning on continuing this! I'll be pushing all of my work (I was careful not to use any of the code set up by Oberlin because of this) to my own repository so I can continue developement. Beyond not using the college's code for it, I was also careful to only utilize tools that explicitly allow commercial use (not that I plan on selling this, it's a fan-made demake, at least I wouldn't without the express permission of Daniel Mullin). I would write more but I fear I'm already past "briefly" describing it, so I'll leave it here.`

## README.md
As part of your submission, complete the responses below. Be sure to include your declaration of the Honor Code at the end of this file.

1. Names of anyone with whom you discussed the final project with:
> Jacob Caney (outside of this class, helped with balancing and playtesting)

2. Honor Code Declaration:
> I have adhered to the honor code in the assignment. - Mya Macke
