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
- check if aws prod does not face cors-issues with websocket prod server. If it does, allow cors (*?)

Nice to have:
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
