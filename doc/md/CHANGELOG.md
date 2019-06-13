Rallyman Online changelog. 

* <a href='#0.0.1'>0.0.1</a> - _2019/06/13_

<hr />

<a name='0.0.1'></a>
### 0.0.1

#### User
* Can sign-up (login, first_name, last_name, email)
* Can sign-in
* Can see `Lobby` page
  * Can see all rallies
  * Can filter rallies according to:
     * `Rally status`
     * `User participation`
     * `Rally creator`
  * Can `Join` opened rallies 
  * Can `Quit` opened rallies to which the user participates 
  * Navigation:
     * Can modify the number of rallies shown by page
     * Can navigate in the list of pages
* Registered users:
  * Can create a rally
  * Edit created rallies:
     * Edit rally planning:
         * Can modify `Rally opens at`, `Rally starts at`
     * Edit rally roadbook: add stages, add sections in stages
* Documentation
  * a
  
#### Superuser

* `Lobby` page:
  * Can delete a `scheduled` rally
  * Can access to the rally backoffice page via a direct link

#### Core

* implemented main models:
  * Configuration models:
     * Skin
     * Zone
  * Live models
     * Participation 
     * Rally
     * Stage
     * GameStep
