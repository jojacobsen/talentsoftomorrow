import { combineReducers } from 'redux'
import { push } from 'react-router-redux'
import { apiBase } from '../utils/apiRequestHelpers'

let refreshTimer
let tokenUpdateRate = 60000
let initialState = {
  username: localStorage.getItem('username'),
  token: localStorage.getItem('user_token'),
  errors: [],
  loggedIn: false,
  isRequesting: false
}

/* ================= */
/* === Actions ===== */
/* ================= */

export const loginSuccesful = (formData, json) => {
  return {
    type: 'LOGIN_SUCCESFUL',
    username: formData.username,
    token: json.token
  }
}

export const loginFailed = (formData, json) => {
  return {
    type: 'LOGIN_FAILED',
    username: 'Sorry ' + formData.username,
    errors: json
  }
}

export const logoutSuccesful = () => {
  return {
    type: 'LOGOUT_SUCCESFUL'
  }
}

export const requestAccess = (formData) => {
  return {
    type: 'REQUEST_ACCESS',
    username: formData.username
  }
}

export const tokenRefreshed = (json) => {
  return {
    type: 'TOKEN_REFRESHED',
    token: json.token
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function authInit () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    if (token) {
      dispatch(refreshToken())
    } else {
      dispatch(push('/login'))
    }
  }
}

export function tryLogin (formData) {
  // Thunk middleware knows how to handle functions.
  // It passes the dispatch method as an argument to the function,
  // thus making it able to dispatch actions itself.

  return function (dispatch) {
    // First dispatch: the app state is updated to inform
    // that the API call is starting.

    dispatch(requestAccess(formData))

    return fetch(apiBase() + '/api-token-auth/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password
        })
      })
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        if (json.token) {
          dispatch(loginSuccesful(formData, json))
          dispatch(push('/dashboard'))
          dispatch(refreshToken())
          localStorage.setItem('user_token', json.token)
          localStorage.setItem('username', formData.username)
        } else {
          dispatch(loginFailed(formData, json))
        }
      })
      .catch((err) => console.log(err))
  }
}

export function logout () {
  return function (dispatch) {
    localStorage.removeItem('user_token')
    localStorage.removeItem('username')
    dispatch(push('/login'))
    clearInterval(refreshTimer)
  }
}

function refreshToken () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    timedRefresh(dispatch, token)

    clearInterval(refreshTimer)
    refreshTimer = setInterval(function () {
      timedRefresh(dispatch, token)
    }, tokenUpdateRate)
  }
}

function timedRefresh (dispatch, token) {
  return fetch(apiBase() + '/api-token-refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      token: token
    })
  }).then((response) => {
    if (response.status > 399) {
      throw new Error('Bad response from server')
    }

    return response.json()
  })
  .then((json) => {
    if (json.token) {
      console.log('token refreshed', new Date(new Date().getTime()).toLocaleTimeString())
      localStorage.setItem('user_token', json.token)
      dispatch(tokenRefreshed(json))
    }
  })
  .catch((err) => {
    console.log('could not refresh token', err)
    dispatch(logout())
  })
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function userInfo (state = initialState, action) {
  switch (action.type) {
    case 'REQUEST_ACCESS':
      return Object.assign({}, state, {
        isRequesting: true
      })

    case 'LOGIN_SUCCESFUL':
      return Object.assign({}, state, {
        username: action.username,
        errors: [],
        loggedIn: true,
        isRequesting: false,
        token: action.token
      })

    case 'LOGOUT_SUCCESFUL':
      return Object.assign({}, state, {
        username: '',
        password: '',
        loggedIn: false,
        token: ''
      })

    case 'LOGIN_FAILED':
      return Object.assign({}, state, {
        username: action.username,
        errors: action.errors.non_field_errors,
        isRequesting: false
      })

    case 'TOKEN_REFRESHED':
      return Object.assign({}, state, {
        token: action.token
      })

    default:
      return state
  }
}

const authReducer = combineReducers({
  userInfo
})

export default authReducer
