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

export const loadPlayers = () => {
  console.log('load players')
  return {
    type: 'LOAD_PLAYERS'
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function players (state = initialState, action) {
  switch (action.type) {
    case 'LOAD_PLAYERS':
    default:
      return state
  }
}

export default players
