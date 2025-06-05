- [X] add typing to all functions, search: 

      def [^\n\)]+([,\(] ?(?!self)(?!cls)[a-z0-9_]+[, =\)]).*?.+: ?\n|( +)def __init__.+(:?\n\1\1.+){0,}(:?\n\1\1self\.\S* ?=)|(def(?! __.+__) .*?\) ?:)|[^:\]\n]+ = lambda

  - [x] ASCII_text.py
  - [x] bosses.py
  - [x] card_library.py
  - [x] card.py
  - [x] deck.py
  - [x] duel.py
  - [x] field.py
  - [x] menu.py
  - [x] QoL.py
  - [X] rogue.py
  - [X] sigils.py
  - [X] remove any easily removed Any annotations
- [ ] allow sigil_sacrifice to replace sigils
- [ ] allow sigil_sacrifice to sacc cards without sigils
- [ ] make merging optional for merge_cards