
const vote = {
    x: 2,
    y: 2,
  }

async function click_vote () {
    // a POST request
    const response = await fetch('http://localhost:8000/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify(vote)
    })

    console.log('status:', response.status)
// output:
//   status: 200
}
