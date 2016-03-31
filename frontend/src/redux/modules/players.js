import { getHeader, apiBase } from '../utils/apiRequestHelpers'
import { reset } from 'redux-form'

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
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    return fetch(apiBase() + '/players/', getHeader(token))
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        dispatch(playersLoaded(json))
      })
      .catch((err) => console.log(err))
  }
}

export function createPlayer () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token
    console.log('createPlayer action')

    dispatch(reset('createPlayer'))
    // debugger
    // return fetch(apiBase() + '/players/', getHeader(token))
    //   .then((response) => {
    //     if (response.status > 400) {
    //       throw new Error('Bad response from server')
    //     }

    //     return response.json()
    //   })
    //   .then((json) => {
    //     dispatch(playersLoaded(json))
    //   })
    //   .catch((err) => console.log(err))
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
