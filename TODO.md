 - [X] create event node class (use enum for event type)

   - 1-3 outgoing, 1-2 ingoing

   - ingoing not strictly necessary, but may make graphics easier with merging

   - need a varient for occupied node, such as where the player starts



 - [X] implement generation of map

   - can't just use l-system: need to allow for merging of different paths

   - will need to heavily rely on ping.txt



 - [X] integrate map into rogue_campaign functionality

   - should only need to store the current node (event most recently chosen)

   - map gen balancing should be done with rogue_campaign instance variables and the event_weight function (or really the choice_fn in general)



 - [X] implement map UI

   - text based

   - you have options: either left or right or you just continue straight
   
     - in addition to a path or looking at deck, you can "look at map", which lets you see what is on each path and what follows