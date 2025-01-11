
function buildBoardFromData(arrayBuffer) {
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
    table.setAttribute('id', 'board_table')
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
                if ( gameStatus == 0) {
                    socket.send(y + " " + x)
                }
              });

            td.appendChild(img)
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    if ( document.getElementById("board").hasChildNodes() ) {
        document.getElementById("board").replaceChild(table, document.getElementById("board").firstChild);
    } else {
        document.getElementById("board").appendChild(table);
    }
    document.getElementById("board").style.marginLeft = parseInt((window.innerWidth - ((gameDimension + 4) * 16)) / 2) + 'px'
}

window.onresize = () => {
    document.getElementById("board").style.marginLeft = parseInt((window.innerWidth - document.getElementById("board_table").offsetWidth) / 2) + 'px'
}

async function loadBoard() {
    const res = await fetch('/board', {
        headers: {
            'Cache-Control': 'no-cache'
        }
    })
    const arrayBuffer = await res.arrayBuffer()
    buildBoardFromData(arrayBuffer)
}

var timer = 30, minutes, seconds;

function startTimer(duration, display) {
    setInterval( () => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}
window.onload = () => {
    startTimer(29, document.getElementById("timer"));
}


const socket = io();  // Connect to the WebSocket server

// when receiving message, apply changes to board and reset timer
socket.on('message', (data) => {
    buildBoardFromData(data)
    timer = 29
})

// Event listener for the open event
socket.on('open', () => {
    console.log('Connected to the WebSocket server');
})

// Event listener for error
socket.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});

// Event listener for close event
socket.addEventListener('close', () => {
    console.log('Disconnected from the WebSocket server');
});


loadBoard()