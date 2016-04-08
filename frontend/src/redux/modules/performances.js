import { postHeader, getHeader, apiBase } from '../utils/apiRequestHelpers'
// import { reset } from 'redux-form'
// import { push } from 'react-router-redux'
import Alert from 'react-s-alert'
// import moment from 'moment'
import { convertObjectToText } from '../utils/reduxHelpers'

const initialState = []

/* ================= */
/* === Actions ===== */
/* ================= */

export const performanceCreated = (json) => {
  return {
    type: 'PERFORMANCE_CREATED',
    performances: json
  }
}

export const performancesLoaded = (json) => {
  return {
    type: 'PERFORMANCES_LOADED',
    performances: json
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */
export function loadPerformances () {
  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token

    return fetch(apiBase() + '/performances/', getHeader(token))
      .then((response) => {
        if (response.status > 400) {
          throw new Error('Bad response from server')
        }

        return response.json()
      })
      .then((json) => {
        dispatch(performancesLoaded(json))
      })
      .catch((err) => {
        Alert.error(err)
      })
  }
}

export function createPerformance (currentData) {
  let tmpCurrentData = currentData

  return function (dispatch, getState) {
    let token = getState().auth.userInfo.token
    let form = getState().form.CreatePerformanceForm
    let formData = form[tmpCurrentData.player.id]
    let playerName = `${tmpCurrentData.player.user.first_name} ${tmpCurrentData.player.user.last_name}`

    let data = {
      value: formData.score.value,
      player: tmpCurrentData.player.id,
      date: '2016-03-12', // TODO: use moment
      measurement: tmpCurrentData.measurement.id,
      description: formData.description.value
    }

    return fetch(apiBase() + '/performances/', postHeader(token, [data]))
      .then((response) => {
        let status = response.status

        if (status > 400) {
          Alert.error(status + ': Bad response from server')
        } else if (status === 400) {
          response.json().then((json) => {
            Alert.error(convertObjectToText(json))
          })
        } else {
          Alert.success(`${playerName}s ${tmpCurrentData.measurement.name.toLowerCase()} er gemt`)
          console.log('performance created')
          dispatch(performanceCreated(data))
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

function performances (state = initialState, action) {
  switch (action.type) {
    case 'PERFORMANCES_LOADED':
      return action.performances
    case 'PERFORMANCE_CREATED':
      return [
        ...state,
        action.performances
      ]
    default:
      return state
  }
}

export default performances
