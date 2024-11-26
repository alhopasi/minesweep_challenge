
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

    const gameStatus = data[0]
    const gameDimension = dataView.getUint16(1)
    
    var table = document.createElement('table')
    for (let y = 0; y < gameDimension; y++) {
        var tr = document.createElement('tr')
        for (let x = 0; x < gameDimension; x++) {
            var td = document.createElement('td')
            td.classList.add('board_inner')
            var img = document.createElement('img')

            var value = boardData[y*gameDimension + x]
            switch (value) {
                case 0:
                    img.src = '/static/images/empty.png'
                case 1:
                    img.src = '/static/images/1.png'
                case 2:
                    img.src = '/static/images/2.png'
                case 3:
                    img.src = '/static/images/3.png'
                case 4:
                    img.src = '/static/images/4.png'
                case 5:
                    img.src = '/static/images/5.png'
                case 6:
                    img.src = '/static/images/6.png'
                case 7:
                    img.src = '/static/images/7.png'
                case 8:
                    img.src = '/static/images/8.png'
                case 9:
                    img.src = '/static/images/mine.png'
                case 10:
                    img.src = '/static/images/mine_exp.png'
                case 11:
                    img.src = '/static/images/unknown.png'
            }
            
            td.appendChild(img)
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    document.getElementById("board").appendChild(table);
    

    //let hexString = '';
    //        for (let i = 0; i < boardData.length; i++) {
    //            hexString += boardData[i].toString(16) + ' ';
    //            if ((i+1) % gameDimension == 0) {
    //                hexString += "\n"
    //            }
    //        }
    //document.getElementById('board').textContent = hexString
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