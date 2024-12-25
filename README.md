### Minesweeper Challenge ###
An attempt to create a multiplayer Minesweeper.

Just for learning and fun


docker-compose up -w


Required:
- timer to update board status (needs more testing that threading works correctly)
- use websockets to update game status online
- send only changed data, not whole board - functions to update only changed data.

Nice to have:
- history of earlier games
- login system for users to keep track of: how many times voted, how many mines stepped into, at what level joined
- nicer gui
- rules page / how it works
- seperate backend from frontend (?)

Minesweeper Tiles from https://kerkday.itch.io/minesweeper-tiles