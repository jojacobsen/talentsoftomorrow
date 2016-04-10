import { getHeader, apiBase } from '../utils/apiRequestHelpers'
import Alert from 'react-s-alert'

const initialState = []

/* ================= */
/* === Actions ===== */
/* ================= */

export const measurementsLoaded = (json) => {
  return {
    type: 'MEASUREMENTS_LOADED',
    measurements: json
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function loadMeasurements () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    return fetch(apiBase() + '/measurements/', getHeader(token))
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        dispatch(measurementsLoaded(json))
      })
      .catch((err) => {
        Alert.error(err)
      })
  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function measurements (state = initialState, action) {
  switch (action.type) {
    case 'MEASUREMENTS_LOADED':
      return action.measurements
    default:
      return state
  }
}

export default measurements
