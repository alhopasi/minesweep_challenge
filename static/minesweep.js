
async function loadBoard() {
    const res = await fetch('/board', {
        headers: {
            'Cache-Control': 'no-cache'
        }
    })
    const arrayBuffer = await res.arrayBuffer()
    const data = new Uint8Array(arrayBuffer)
    const dataView = new DataView(arrayBuffer)
    const boardData = data.slice(3)

    let gameStatus = data[0]
    let gameDimension = dataView.getUint16(1)
    
    let hexString = '';
            for (let i = 0; i < boardData.length; i++) {
                hexString += boardData[i].toString(16) + ' ';
                if ((i+1) % gameDimension == 0) {
                    hexString += "\n"
                }
            }
    document.getElementById('board').textContent = hexString
}


async function click_vote () {

    const vote = {
        x: 2,
        y: 2,
    }

    const response = await fetch('http://localhost:8000/vote', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify(vote)
    })

    console.log('status:', response.status)
}

loadBoard()