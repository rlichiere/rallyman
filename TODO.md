
#### Mandatory

* implement sections connections (input to output anchors)
  * this will be required to manage map connections
* implement position of participants in rally
  * manage first_turn while closeGameStep to make each player plays N times at the first turn of a stage

<hr />

#### Quick

* add persistence option to create rally form
* add `rally-edit-advanced` page to manage:
  * persistence
  * privacy options
  * participants start order method:
     * `by_experience`: sort participants by their number of travelled cells
     * `by_registration_order`: sort participants by order of registration
     * `by_creator`: allows only the creator of the rally to sort the participants.
            The participants who are not placed by the creator are sorted by experience, otherwise by order of registration
     * `from_rally_order`: Sort participants according to the order used in a previous rally.
             The participants who did not participate to the previous rally are placed at end,
                ordered by order of registration
     * `from_rally_result`: Sort participants according to the result of a previous rally.
            The participants who did not participate to the previous rally are placed at end,
                ordered by experience, otherwise by order of registration
     * `from_rally_result_reverse`: Sort participants according to the reversed result of a previous rally
            The participants who did not participate to the previous rally are placed at first,
            ordered by experience reversed, otherwise by order of registration reversed
* add `link_to_bo` where it can be usefull for the superusers
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
