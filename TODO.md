 - [ ] create event node class (use enum for event type)

   - 1-3 outgoing, 1-2 ingoing

   - ingoing not strictly necessary, but may make graphics easier with merging

   - need a varient for occupied node, such as where the player starts



 - [ ] implement generation of map

   - can't just use l-system: need to allow for merging of different paths

   - will need to heavily rely on ping.txt



 - [ ] integrate map into rogue_campaign functionality

   - should only need to store the current node (event most recently chosen)



 - [ ] impliment ASCII visuals

   - each event type will need an icon