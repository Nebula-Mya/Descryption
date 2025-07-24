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



 - [ ] impliment ASCII visuals

   - each event type will need an icon

   - use an X (larger) for where the player is / has been

   - display vertically, allow scrolling (will worry about making it feel DOS-Y when im not actually working through the terminal aka post rust)

   - have prebuilt strings for increasing/decrease by 1 to 2,3,4,5,6,7 (only increase to 7), allowing for events to be shared or not, then they can be pieced together to form the map