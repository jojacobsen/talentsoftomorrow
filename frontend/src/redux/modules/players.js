import { getHeader, apiBase } from '../utils/apiRequestHelpers'

/* ================= */
/* === Actions ===== */
/* ================= */

export const playersLoaded = (json) => {
  return {
    type: 'PLAYERS_LOADED',
    players: json
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function loadPlayers () {
  return function (dispatch) {
    return fetch(apiBase() + '/players/', getHeader)
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        dispatch(playersLoaded(json))
      })
      .catch((err) => alert(err))
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function players (state = [], action) {
  switch (action.type) {
    case 'PLAYERS_LOADED':
      return action.players
    default:
      return state
  }
}

export default players
