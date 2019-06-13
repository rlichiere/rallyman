
#### Mandatory

* add Rally update form (label, opened_at, started_at)
* implement sections connections (input to output anchors)
  * this will be required to manage map connections
* implement position of participants in rally
  * manage first_turn while closeGameStep to make each player plays N times at the first turn of a stage

<hr />

#### Quick

* add link-to-backoffice where it can be usefull for the superusers
* add a debug menu to manage:
  * console features (show)
     * choose logging level: verbose/debug/info/warning/error
     * search errors button
  * ping of backend availability
     * on/off
     * refresh delay change

<hr />

#### Later
  
* GameUI
  * implement the game layout 
  * implement the map layout (must be able to combine several zones)
* GameLogic
  * implement the complete game process:
     1. OK - Initialize game data
     1. OK - Place participants on track
     1. OK - Start the game by giving the hand to the first player on track
     1. Manage this player play
     1. Elect the next participant (the next car on the track)
     1. TEST - Repeat from e. until all cars have finished the stage
     1. Process the results and close the game
