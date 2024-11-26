### Minesweeper Challenge ###
An attempt to create a multiplayer Minesweeper.

Just for learning and fun


docker-compose up -w


Required:
- draw border tiles on board
- clickable tiles to front to vote which tile to flip
- timer to update board status
- voting to select which tiles to flip
- when flipping a '0' tile, flip those around it -> repeat until no more 0'es.
- when flipping a mine -> end game -> display all mines and those that were flipped -> generate new game on next update

Nice to have:
- history of earlier games
- login system for users to keep track of: how many times voted, how many mines stepped into, at what level joined
- nicer gui
- rules page / how it works
- seperate backend from frontend (?)

Minesweeper Tiles from https://kerkday.itch.io/minesweeper-tiles