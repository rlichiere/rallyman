# Rallyman

Python/Django implementation of the famous board game **_[Rallyman](http://rallyman.fr/)_** created by **J.-C. Bouvier**.
Thank you to him, may joy and happiness iridesce his life.

This implementation is based on the 2nd edition of the game (November 2009), with the objective of covering all the rules of this version.

Additional functionalities are planned and will concern the side events:
no change will be made to the original rules governing the conduct of the games.


Uses:
* Python 2.7
* Django 1.9
* Bootstrap 4


## Main features

Below, the non-exhaustive list of features planned to be implemented in this application:

* Game modes
  * Solo game
  * Multiplayer game, up to 4 players
* Game features
  * Game creation
    * Roadbook configuration
      * Configuration of the stages of the rally
      * Configuration of the sections of each stage
      * Ability to plan repair assistance at the end of chosen stages
      * Ability to configure random weather
        * The probability of an unexpected change of the surface can be configured for each stage or section
      * Display of the length in cells of each stage, and of the complete rally
      * Ability to initiate from a roadbook template
        * From creator's templates
        * From public templates
    * Planning configuration
      * Scheduled game: delays the players registration to a specific date,
        otherwise the registration is available immediately
      * Game start mode: delays the start of the game to a specific data,
        otherwise the game starts when all slots are reserved by players
    * Public/private games
      * a **public game** is accessible to **any registered user**
      * a **private game** is only accessible to **players chosen by the creator**
        * Authorized players can be selected individually, or by opening up to the creator's direct contacts
      * Players can join all public games by themselves, or by invitation from the creator or a participant of a game
      * Players can join private games only by invitation from the creator
    * Rules and regulations
      * The original game provides a general rulebook composed of 12 mandatory articles, accompanied by 4 optional articles (`Rules +`)
        * The creation of a rally proposes to select the optional `Rules +` that will apply in addition to the mandatory articles:
          * Article 13: Weather and tyres
          * Article 14: Big attack
          * Article 15: Drop of seconds
          * Article 16: Split times
        * All participants are subject to the selected rules, there are no exceptions.
    * ELO mode
      * forces the participation of the game's creator
      * limits the rally to 2 participants (1-vs-1)
      * Ability to select the joining mode
        * _Free_: the game is opened to any player, by a selection in the list of joignable games 
        * _Closest ELO_: the game is joignable only by the _Search ELO game_ button
          * When a user searches a ELO game, the system selects a game for which the competitor has the score closest to that of the player
          * 
        * _Both_: The two ways to join the game are possible (_Free_ and _Closest ELO_) 
  * Game modification
    * The game creator can modify the label, roadbook and planning configuration as long as the game is not opened
    * One the game is open for registration, the creator can no longer modify the game's properties
  * Game deletion
    * Deletion of a game is authorized if these conditions are met:
      * available only for creator of the game
      * the game is not started nor finished 
      * running and finished games can only be deleted by a superadmin
  * Game history
    * All games are stored in the archive database
    * The course of the games is archived, which makes it possible to replay the games later on
      * The replay is available to the game's participants, or to all users if the creator decides so
      * For privacy and competitiveness reasons, there are currently no plans to be able to access to the replay of a running game
  * Championships
    * Possibility to create championships
      * Composed of multiples rallies
      * Opened to individual players or to teams
      * Grid points customizable by the creator
  * Roadbook templates
    * Ability to create/edit/delete roadbook templates
      * Public
      * Private
    * Modifying a scored templates resets its score
  * Persisting rallies
    * Can only be created by superusers
    * Restarts automatically when finished, with a configurable opening time range
    * Can be eligible to WR achievements by configuration
      * Removing a persisting rally from the list of items eligible for WR
        * do not delete WR timings
        * do not delete WR achievements
      * Deleting a persisting template
        * deletes related WR timings
        * do not delete WR achievements
  * Ability to give a score (between 1 and 10) to public templates
* Player profile
  * Ability to modify user's first name, last name, email and password
  * Display of user's statistics
    * Number of participated rallies
      * Ratio of finished/participations rallies
      * Ratio of won/participations rallies
    * Total distance covered (in cells)
    * Number of won rallies, grouped by
      * Private rallies
      * Public rallies
      * Championships
    * Number of off-roads
      * Total
      * Average per rally
      * Average by distance (in cells)
    * Number of flat punctures
      * Total
      * Average per rally
      * Average by distance (in cells)
    * Number of broken gears
      * Total
      * Average per rally
      * Average by distance (in cells)
    * Number of flags
      * Total
      * Average per rally
      * Average per distance (in cells)
      * Ratio of flags/die roll
      * Ratio of crash/flags
    * Number of created rallies and championships
      * Public
      * Private
  * Achievements
    * Several achievements can be unlocked while playing the game, according to below game events:
      * Each zone used
      * Each stage used
      * All zones used
      * All stages used
      * Rallies participated
      * Rallies finished
      * Rallies won
      * Championships participated
      * Championships finished
      * Championships won
      * ELO participated
      * ELO finished
      * ELO won
      * Overtakes
      * WR breaking
      * Rally winner
      * Dice 5 user
      * Double gaz user
      * Gear crash
      * Second gear crash
      * Third gear crash
      * Car crash
      * Puncture
      * Double puncture
      * Triple puncture (possible ?)
      * Big attack user
      * Drop of seconds user
      * Seconds dropped
    * Each achievement counter unlocks 21 levels distributed in 7 categories : 
      * Steel   :       1,        2,       5,
      * Bronze  :      10,       20,      50,
      * Silver  :     100,      200,     500,
      * Gold    :    1000,     2000,    5000,
      * Platinum:   10000,    20000,   50000,
      * Diamond :  100000,   200000,  500000,
      * Master  : 1000000,  2000000, 5000000
    * Each category has its own medal in the form of a dedicated icon
      * This icon has 3 derivations according to corresponding (1x, 2x or 5x)
    * The user can select one of its medals as a public profile medal
      * The user profile medal is used next to the user name in several game interfaces
  * ELO
    * A ELO ranking applies to 1-vs-1 games created with ELO option
    * The ELO ranking is shown publicly


## Installation

### Install prerequisites

* Install Python 2.7
* Install Django 
   ```shell
   pip install Django
   ```

### Prepare application configuration

* Edit `config/config.yml`
  * Configure the type and connection parameters for the application database
  * Configure the static application presets (max participants per rally, etc)

### Initialize application
   
* Migrate
  ```shell
  python manage.py migrate
  ```
* Create the administrator account
  ```shell
  python manage.py createsuperuser
  ```
* Create initial models
  ```shell
  python manage.py loaddata install/initial.json
  ```

### Run

```shell
python manage.py runserver localhost:8000
```


## Tools

### Backup/Restore

* Backup the database content
  ```shell
  python manage.py dumpdata --indent 2 --exclude auth.permission --exclude sessions.session --exclude admin.logentry --exclude contenttypes > backup/backup.json
  ```
* Backup the configuration of the application
  ```shell
  python manage.py configuration backup --file backup.zip --confirm 
  ```
* Restore the database content
  ```shell
  python manage.py loaddata backup/backup.json
  ```
* Restore the configuration of the application
  ```shell
  python manage.py configuration restore --file backup.zip --confirm 
  ```


## Changelog




## Todo

* Mandatory
  * add Rally update form (label, opened_at, started_at)
  * Console:
    * implement _Close console_ button
    * implement _Increase_/_Reduce_ console height buttons
* Quick
  * implement the configuration loader

* Later
  * GameUI
    * implement the game layout 
    * implement the map layout (must be able to combine several zones)
  * GameLogic
    * implement the game process:
      1. Initialize game data
      2. Place participants on track
      3. Play 1 turn of dices to define the start order of the participants
      4. Start the game by giving the hand to the first player on track
  --> 5. Manage this player play
  |   6. Elect the next participant (the next car on the track)
  |-< 7. Repeat until all cars have finished the stage
      8. Process the results and close the game

