import { postHeader, getHeader, apiBase } from '../utils/apiRequestHelpers'
import Alert from 'react-s-alert'
import moment from 'moment'
import { convertObjectToText } from '../utils/reduxHelpers'


const initialState = []

/* ================= */
/* === Actions ===== */
/* ================= */

export const performanceCreated = (json) => {
  return {
    type: 'PERFORMANCE_CREATED',
    performance: json
  }
}

export const performancesLoaded = (json) => {
  return {
    type: 'PERFORMANCES_LOADED',
    performances: json
  }
}

export const changePerformanceStatus = (data) => {
  return {
    type: 'CHANGE_PERFORMANCE_STATUS',
    id: data.id,
    status: data.status
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
    let playerId = tmpCurrentData.player.id
    let measurementId = tmpCurrentData.measurement.id
    let data = {
      value: formData.score.value,
      player: playerId,
      date: moment().format('YYYY-MM-DD'),
      measurement: measurementId,
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

function statusFilter (date) {
  let cooledDown = moment(date).isBefore(moment(), 'day')

  if(cooledDown) {
     return 'CREATE'
  } else {
    return 'SHOW'
  }
}

function performance (state, action) {
 switch (action.type) {
    case 'PERFORMANCES_LOADED':
      return {
        ...state,
        status: statusFilter(state.date)
      }
    case 'PERFORMANCE_CREATED':
      return {
        ...action.performance,
        status: statusFilter(action.date)
      }
    case 'CHANGE_PERFORMANCE_STATUS':
      console.log(state.id, action.id)
      if (state.id === parseInt(action.id)) {
        return Object.assign({}, state, {
          status: action.status
        })
      } else {
        return state
      }
    default:
      return state
  }
}

function performances (state = initialState, action) {
  switch (action.type) {
    case 'PERFORMANCES_LOADED':
      return action.performances.map((p) => performance(p, action))
    case 'PERFORMANCE_CREATED':
      return [
        ...state,
        performance(undefined, action)
      ]
    case 'CHANGE_PERFORMANCE_STATUS':
      return state.map((p) => performance(p, action))
    default:
      return state
  }
}

export default performances
