import { getHeader, postHeader, apiBase } from '../utils/apiRequestHelpers'
import { reset } from 'redux-form'
import { push } from 'react-router-redux'

/* ================= */
/* === Actions ===== */
/* ================= */

export const playersLoaded = (json) => {
  return {
    type: 'PLAYERS_LOADED',
    players: json
  }
}

export const playerAdded = (json) => {
  return {
    type: 'PLAYER_ADDED'
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
    let form = getState().form.createPlayer
    let token = getState().auth.userInfo.token
    let username = 'user' + Math.floor((Math.random() * 999999) + 1)
    let json = [
      {
        user: {
          username: username,
          last_name: form.last_name.value,
          first_name: form.first_name.value
        },
        gender: form.gender.value,
        date_of_birth: form.birthday.value,
        coach: [parseInt(form.coaches.value)], // TODO: make array-able
        club: 1 // TODO: remove
      }
    ]

    return fetch(apiBase() + '/players/', postHeader(token, json))
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        } else if (response.status === 400) {
          response.json().then((json) => {
            console.log('validation error', json)
            // Handle validation errors
          })
        } else {
          response.json().then((json) => {
            console.log('success', json)
            dispatch(playerAdded(json))
            dispatch(reset('createPlayer'))
            dispatch(push('/talents'))
          })
        }
      })
      .catch((err) => {
        console.log(err)
      })
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
