let initialState = {
  players: [
    {
      id: 1,
      first_name: 'Tobias',
      last_name: 'Pedersen',
      birthday: 1464004800
    },
    {
      id: 2,
      first_name: 'Lionel',
      last_name: 'Messi',
      birthday: 1464004800
    }
  ]
}

/* ================= */
/* === Actions ===== */
/* ================= */

export const playersLoaded = () => {
  console.log('players loaded')
  return {
    type: 'PLAYERS_LOADED'
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function loadPlayers () {
  let authHeader = `JWT ${localStorage.getItem('user_token')}`
  console.log(authHeader)

  return function (dispatch) {
    return fetch('http://127.0.0.1:8000/player/',
      {
        mode: 'cors',
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authHeader,
        }
      })
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        console.log(json)
      })
      .catch((err) => alert(err))
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function players (state = initialState, action) {
  switch (action.type) {
    case 'PLAYERS_LOADED':
    default:
      return state
  }
}

export default players
