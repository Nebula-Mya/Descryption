from __future__ import annotations # prevent type hints needing import at runtime
from typing import TYPE_CHECKING

from enum import Enum

class Event_Type(Enum):
    CURRENT = 0
    CARD_CHOICE = 1
    SIGIL_SACRIFICE = 2
    MERGE_CARDS = 3
    PELT_SHOP = 4
    CARD_SHOP = 5
    BREAK_ROCKS = 6
    CAMPFIRE = 7
    CARD_BATTLE = 8

    def __eq__(self, other: Event_Type) :
        return self.value == other.value

class Event_Node:
    type: Event_Type
    ins: list[Event_Node]
    outs: list[Event_Node]

    def __init__(self, type_id: int) -> None :
        self.type = Event_Type(type_id)
        self.ins = []
        self.outs = []

    def add_in(self, new_in: Event_Node) -> bool :
        if len(self.ins) >= 2 : return False

        self.ins.append(new_in)

        return True
    
    def rem_in(self) -> bool :
        if len(self.ins) <=0 : return False

        self.ins.pop()

        return True

    def add_out(self, new_out: Event_Node) -> bool :
        if len(self.outs) >= 3 : return False

        self.outs.append(new_out)

        return True
    
    def rem_out(self) -> bool :
        if len(self.outs) <=0 : return False
        
        self.outs.pop()

        return True