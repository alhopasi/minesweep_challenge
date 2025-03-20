### Minesweeper Challenge ###
An attempt to create a multiplayer Minesweeper

Just for learning and fun

replace <ENV> with 'dev' or 'prod' for Development or Production environment
Build: docker compose -f compose.<ENV>.yaml build
Run: docker compose -f compose.<ENV>.yaml up

Connect to http://localhost:5000 for Dev environment
Connect to http://localhost for Production environment


Online version running in https://theminesweep.com


#### How it works ####
- Click on tile to vote
- Votes are counted and the tiles with most votes get explored
- Max explored tiles / tick is board dimension / 4. (100x100 board = 100/4 = 25)
- If votes are tied for a tile, the order gets randomized in which they are explored
- You can only vote for one tile / IP address for each tick
- Ticks run every 10 seconds
- If all empty tiles are explored, players win and the board dimension increases by 1
- If a mine gets explored, players lose and the board resets at same dimension


#### Development ####

Next:
- database:
  - user-entity:
    - username (id)
    - password
    - total score
    - mine hits
    - explored tiles (incl. bombs)
    - participated in levels (list) + score for each level
    - last gametick
    - consecutive successful explorations (score streak)
    - score level (min 1)
    - victories (explored tile on turn when the board was victorius)
    - admin flag
  - gametick (increment by 1 when game ticks)

- user web ui / backend
  - create new user
  - login with username and password
  - logout (when logged in)
  - user page (when logged in)
    - change password option
    - delete user option
  - admin options:
    - list users
    - delete user
    - change game level / reset current level

- score system:
  - score gets saved if the user is logged in. Otherwise it's temporary.
  - each level has a scoreboard (show top 20, ordered by points + victories).
  - if a mine is hit, the scoreboard is cleared.
  - if victory, save top 20 scores as scoreboard
  - score streak:
    - if missed gameticks, decrease score streak by missed ticks amount:
      - score_streak = last_gametick - current_gametick + 1
    - if hit mine:
      - score_streak -= score_level
    - else: score_streak += 1
    - if score_streak == score_level, increase level:
      - score_level += 1, score_streak = 0
    - while score_streak < 0:
      - score_level -= 1, score_streak += score_level  (if score_level == 1 && score_streak <= 0, end)
    - give score to player according to score level.
      - if player was only one who voted a tile (and it got explored), give double points
      - if given_score < victories: given_score = victories
    
- level history
  - save gameboard when victory / loss
  - save scoreboard when victory
  - web ui page to show finished level / scoreboard, example:
  - level 10 (current)
    - board 2 - mine_exp_image - turn 21
    - board 1 - mine_exp_image - turn 2
  - level 9
    - board 3 - mine_image - turn 34
    - board 2 - mine_exp_image - turn 4
    - board 1 - mine_exp_image - turn 1
  - level 8 ....

- Hall Of Fame
  - Show all top score players for previous levels
  - Show top 100 players
  - Sort by: Total Score, Victories




Nice to have:
- reputation system for user (if user has triggered mines, users votes don't count unless the user makes 'good' votes)
- nicer gui:
  - split view horizontally into top header (menu / info) and bottom board.
  - send info how many votes was sent on previous tick
  - rules page / how it works
- history of earlier games
- login system for users to keep track of: how many times voted, how many mines stepped into, at what level joined



Info:
- Development environment uses Docker volumes for source code to load from, making easy changes possible, not needing to build the whole container
- Production environment has all source code bundled in the Docker container.
- ./data is used as volume for persistent storage to save board data, and also using ./data/online to save online board data.

Minesweeper Tiles from https://kerkday.itch.io/minesweeper-tiles
