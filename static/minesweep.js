var gameStatus
var tintTile

function parseData(arrayBuffer) {
    const dataView = new DataView(arrayBuffer)
    
    // load 13 leftmost bits as gameDimension and 3 rightmost bits as gameStatus
    const gameData = dataView.getUint16(0)
    const gameDimension = gameData >> 3
    gameStatus = gameData & 7

    const data = new Uint8Array(arrayBuffer)
    const boardData = data.slice(2)
    
    if (document.getElementById('board_table') == null || gameStatus == 3) {
        buildBoardFromData(boardData, gameDimension)
    } else {
        updateBoardFromData(boardData, gameDimension)
    }
    clearTint()
}

function buildBoardFromData(boardData, gameDimension) {

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
    table.setAttribute('id', 'board_table')
    for (let y = -2; y < gameDimension + 2; y++) {
        var tr = document.createElement('tr')
        for (let x = -2; x < gameDimension + 2; x++) {
            var td = document.createElement('td')
            td.classList.add('board_inner')

            if (x < 0 || x >= gameDimension || y < 0 || y >= gameDimension) {
                var img = document.createElement('img')
                img.src = '/static/images/wall.png'
                td.appendChild(img)
                tr.appendChild(td)
                continue
            }

            var value = gameBoardValues[y][x]
            var img = setImage(value)

            img.addEventListener('click', function (e) {
                if ( gameStatus == 0 || gameStatus == 3) {
                    socket.send(y + " " + x)
                    addTint(y*gameDimension + x)
                }
              });

            td.appendChild(img)
            td.setAttribute('id', "tile" + parseInt(y*gameDimension + x))
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    if ( document.getElementById('board').hasChildNodes() ) {
        document.getElementById('board').replaceChild(table, document.getElementById('board').firstChild);
    } else {
        document.getElementById('board').appendChild(table);
    }
    document.getElementById('board').style.marginLeft = parseInt((window.innerWidth - ((gameDimension + 4) * 16)) / 2) + 'px'
}

function clearTint() {
    if (document.getElementById('tile' + tintTile) && document.getElementById('tile' + tintTile).classList && document.getElementById('tile' + tintTile).classList.contains('tint')) {
        document.getElementById('tile' + tintTile).classList.remove('tint');
      }
}

function addTint(tileValue) {
    clearTint()
    document.getElementById('tile' + parseInt(tileValue)).classList.add('tint')
    tintTile = tileValue
}

function setImage(tileValue) {
    var img = document.createElement('img')
    switch (tileValue) {
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
    return img
}

var windowWidth = window.innerWidth

window.onresize = () => {
    if (window.innerWidth != windowWidth) {
        windowWidth = window.innerWidth
        document.getElementById('board').style.marginLeft = parseInt((window.innerWidth - document.getElementById('board_table').offsetWidth) / 2) + 'px'
    }
}

async function loadBoard() {
    const res = await fetch('/board', {
        headers: {
            'Cache-Control': 'no-cache'
        }
    })
    const arrayBuffer = await res.arrayBuffer()
    parseData(arrayBuffer)
}

function updateBoardFromData(boardData, gameDimension) {
    const tileNumberBytes = calculateBytesNeeded(gameDimension)
    var tileNumber = 0
    var byteNumber = 0

    for (let i = 0; i < boardData.length; i++) {
        
        if (byteNumber < tileNumberBytes) {
            shiftAmount = 8 * byteNumber
            value = boardData[i]
            valueToAdd = value << shiftAmount
            tileNumber = tileNumber + valueToAdd
            byteNumber += 1
            continue
        } else {
            var td = document.getElementById('tile' + parseInt(tileNumber))
            td.removeChild(td.firstChild)
            var img = setImage(boardData[i])
            td.appendChild(img)
            tileNumber = 0
            byteNumber = 0
        }
    }
}

function calculateBytesNeeded(gameDimension) {
    var result = 0
    while (gameDimension > 1) {
        gameDimension = gameDimension / 16
        result += 1
    }
    return result
}

var timer = 10, minutes, seconds;

function startTimer(duration, display) {
    setInterval( () => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}
window.onload = () => {
    startTimer(9, document.getElementById('timer'));
}

const socket = io(window.location.origin, {
    transports: ['websocket']  // Force WebSocket transport
});  // Connect to the WebSocket server

  
// when receiving message, apply changes to board and reset timer
socket.on('message', (data) => {
    parseData(data)
    timer = 9
})


loadBoard()