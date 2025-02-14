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
- As many tiles get explored at most, as many the dimension of the board is. ex. if board is 10x10, the amount of explored tiles is at most 10
- If votes are tied for a tile, the order gets randomized in which they are explored
- You can only vote once / IP address for each tick
- Ticks run every 30 seconds
- If all empty tiles are explored, players win and the board dimension increases by 1
- If a mine gets explored, players lose and the board resets at same dimension


#### Development ####
Required:
- set up Gunicorn to use with prod environment

Nice to have:
- send info how many votes was sent on previous tick
- nicer gui
- history of earlier games
- login system for users to keep track of: how many times voted, how many mines stepped into, at what level joined
- rules page / how it works

Info:
- Development environment uses Docker volumes for source code to load from, making easy changes possible, not needing to build the whole container
- Production environment has all source code bundled in the Docker container.
- ./data is used as volume for persistent storage to save board data, and also using ./data/online to save online board data.

Minesweeper Tiles from https://kerkday.itch.io/minesweeper-tiles
