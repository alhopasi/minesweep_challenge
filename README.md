### Minesweeper Challenge ###
An attempt to create a multiplayer Minesweeper.

Just for learning and fun

replace <ENV> with 'dev' or 'prod' for Development or Production environment
Build: docker compose -f compose.<ENV>.yaml build
Run: docker compose -f compose.<ENV>.yaml up

Connect to http://localhost:5000 for Dev environment
Connect to http://localhost for Production environment


Required:
- voting with IP does not work in Docker Localhost, deploy to internet to see if X-Forwarded-For header delivers the correct IP

Nice to have:
- better timer to update board status (better way to implement?)
- when loading page - load whole board with HTTP request. When updating board - only update changed with websockets. When reset (victory or loss) - update whole board with websocket.
- nicer gui
- history of earlier games
- login system for users to keep track of: how many times voted, how many mines stepped into, at what level joined
- rules page / how it works
- seperate backend from frontend (?)

Deploy to internet:
- with github actions automate workflow to push new version to aws ecs?
- domain name for the web app
- use aws load balancer for ssl certificate and https connection

Minesweeper Tiles from https://kerkday.itch.io/minesweeper-tiles