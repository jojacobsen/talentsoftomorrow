import { getHeader, apiBase } from '../utils/apiRequestHelpers'
import Alert from 'react-s-alert'

const initialState = []

/* ================= */
/* === Actions ===== */
/* ================= */

export const coachesLoaded = (json) => {
  return {
    type: 'COACHES_LOADED',
    coaches: json
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function loadCoaches () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    return fetch(apiBase() + '/coaches/', getHeader(token))
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        dispatch(coachesLoaded(json))
      })
      .catch((err) => {
        Alert.error(err)
      })
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function coaches (state = initialState, action) {
  switch (action.type) {
    case 'COACHES_LOADED':
      return action.coaches
    default:
      return state
  }
}

export default coaches