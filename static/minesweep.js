
async function loadBoard() {
    const res = await fetch('/board', {
        headers: {
            'Cache-Control': 'no-cache'
        }
    })
    const arrayBuffer = await res.arrayBuffer()
    const data = new Uint8Array(arrayBuffer)
    const dataView = new DataView(arrayBuffer)
    const boardData = data.slice(2)

    // load 14 leftmost bits as gameDimension and 2 rightmost bits as gameStatus
    const gameData = dataView.getUint16(0)
    const gameDimension = gameData >> 2
    const gameStatus = gameData & 3
    
    let y = 0
    let x = 0

    let gameBoardValues = Array.from({ length: gameDimension }, () => Array(gameDimension).fill(undefined));

    for (let i = 0; i < boardData.length; i++) {
        first = boardData[i] >> 4
        second = boardData[i] & 15
        if (x >= gameDimension) {
            x = 0
            y += 1
        }
        gameBoardValues[y][x] = first
        x += 1

        if (second == 15) {
            continue
        }

        if (x >= gameDimension) {
            x = 0
            y += 1
        }
        gameBoardValues[y][x] = second
        x += 1
    }

    var table = document.createElement('table')
    for (let y = -2; y < gameDimension + 2; y++) {
        var tr = document.createElement('tr')
        for (let x = -2; x < gameDimension + 2; x++) {
            var td = document.createElement('td')
            td.classList.add('board_inner')
            var img = document.createElement('img')

            if (x < 0 || x >= gameDimension || y < 0 || y >= gameDimension) {
                img.src = '/static/images/wall.png'
                td.appendChild(img)
                tr.appendChild(td)
                continue
            }


            var value = gameBoardValues[y][x]
            switch (value) {
                case 0:
                    img.src = '/static/images/empty.png'
                    break
                case 1:
                    img.src = '/static/images/1.png'
                    break
                case 2:
                    img.src = '/static/images/2.png'
                    break
                case 3:
                    img.src = '/static/images/3.png'
                    break
                case 4:
                    img.src = '/static/images/4.png'
                    break
                case 5:
                    img.src = '/static/images/5.png'
                    break
                case 6:
                    img.src = '/static/images/6.png'
                    break
                case 7:
                    img.src = '/static/images/7.png'
                    break
                case 8:
                    img.src = '/static/images/8.png'
                    break
                case 9:
                    img.src = '/static/images/unknown.png'
                    break
                case 10:
                    img.src = '/static/images/mine.png'
                    break
                case 11:
                    img.src = '/static/images/mine_exp.png'
            }

            img.addEventListener('click', function (e) {
                vote(y, x)
              });

            td.appendChild(img)
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    document.getElementById("board").appendChild(table);

}


async function vote (y, x) {

    const vote = {
        y: y,
        x: x
    }

    const response = await fetch('http://localhost:8000/vote', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify(vote)
    })

}

loadBoard()