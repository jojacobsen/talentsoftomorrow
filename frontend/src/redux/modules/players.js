import { getHeader, postHeader, apiBase } from '../utils/apiRequestHelpers'
import { reset } from 'redux-form'
import { push } from 'react-router-redux'
import Alert from 'react-s-alert'
import { convertObjectToText } from '../utils/reduxHelpers'

const initialState = []

/* ================= */
/* === Actions ===== */
/* ================= */

export const playersLoaded = (json) => {
  return {
    type: 'PLAYERS_LOADED',
    players: json
  }
}

export const playerAdded = () => {
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
      .catch((err) => {
        Alert.error(err)
      })
  }
}

export function createPlayer () {
  return function (dispatch, getState) {
    let form = getState().form.CreatePlayer
    let token = getState().auth.userInfo.token
    let username = 'user' + Math.floor((Math.random() * 999999) + 1)
    let data = [
      {
        user: {
          username: username,
          last_name: form.last_name.value,
          first_name: form.first_name.value
        },
        gender: form.gender.value,
        birthday: form.birthday.value,
        coaches: [parseInt(form.coaches.value)],
        club: 1 // TODO: remove
      }
    ]

    return fetch(apiBase() + '/players/', postHeader(token, data))
      .then((response) => {
        let status = response.status

        if (status > 400) {
          Alert.error(status + ': Bad response from server')
        } else if (status === 400) {
          response.json().then((json) => {
            Alert.error(convertObjectToText(json))
          })
        } else {
          console.log('player created')
          dispatch(playerAdded(data))
          dispatch(reset('createPlayer'))
          dispatch(push('/talents'))
        }
      })
      .catch((err) => {
        Alert.error(err)
      })
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function players (state = initialState, action) {
  switch (action.type) {
    case 'PLAYERS_LOADED':
      return action.players
    default:
      return state
  }
}

export default players
