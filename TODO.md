- [X] add typing to all functions, search: 

      def [^\n\)]+([,\(] ?(?!self)(?!cls)[a-z0-9_]+[, =\)]).*?.+: ?\n|( +)def __init__.+(:?\n\1\1.+){0,}(:?\n\1\1self\.\S* ?=)|(def(?! __.+__) .*?\) ?:)|[^:\]\n]+ = lambda

  - [X] ASCII_text.py
  - [X] bosses.py
  - [X] card_library.py
  - [X] card.py
  - [X] deck.py
  - [X] duel.py
  - [X] field.py
  - [X] menu.py
  - [X] QoL.py
  - [X] rogue.py
  - [X] sigils.py
  - [X] remove any easily removed Any annotations
- [ ] allow sigil_sacrifice to replace sigils
- [ ] allow sigil_sacrifice to sacc cards without sigils
- [X] prevent softlock if merging with no duplicates