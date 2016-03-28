import { combineReducers } from 'redux'
import { push } from 'react-router-redux'

let initialState = {
  username: localStorage.getItem('username'),
  password: '',
  token: '',
  errors: [],
  loggedIn: false,
  isRequesting: false
}
let tokenUpdateRate = 5000
let refreshTimer

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

/* ================= */
/* === Thunks ====== */
/* ================= */

export function tryLogin (formData) {
  // Thunk middleware knows how to handle functions.
  // It passes the dispatch method as an argument to the function,
  // thus making it able to dispatch actions itself.

  return function (dispatch) {
    // First dispatch: the app state is updated to inform
    // that the API call is starting.

    dispatch(requestAccess(formData))

    return fetch('http://127.0.0.1:8000/api-token-auth/',
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
          console.log(json.token)
          dispatch(loginSuccesful(formData, json))
          dispatch(push('/dashboard'))
          dispatch(refreshToken(formData))
          localStorage.setItem('user_token', json.token)
          localStorage.setItem('username', formData.username)
        } else {
          dispatch(loginFailed(formData, json))
        }
      })
      .catch((err) => alert(err))
  }
}

export function logout () {
  return function (dispatch) {
    localStorage.removeItem('user_token')
    localStorage.removeItem('username')
    dispatch(push('/login'))
    clearTimeout(refreshTimer)
  }
}

/* ================= */
/* ===== Utils ===== */
/* ================= */

function refreshToken (formData) {
  return function (dispatch) {
    refreshTimer = setTimeout(function () {
      dispatch(tryLogin(formData))
      console.log('refreshToken')
    }, tokenUpdateRate)
  }
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
        isRequesting: false
      })

    case 'LOGOUT_SUCCESFUL':
      return Object.assign({}, state, {
        username: '',
        password: '',
        loggedIn: false
      })

    case 'LOGIN_FAILED':
      return Object.assign({}, state, {
        username: action.username,
        errors: action.errors.non_field_errors,
        isRequesting: false
      })

    default:
      return state
  }
}

const authReducer = combineReducers({
  userInfo
})

export default authReducer
