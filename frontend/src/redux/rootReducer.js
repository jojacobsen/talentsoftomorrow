import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'
import {reducer as formReducer} from 'redux-form'
import auth from './modules/auth'
import players from './modules/players'
import coaches from './modules/coaches'
import measurements from './modules/measurements'

export default combineReducers({
  router,
  form: formReducer,
  auth,
  players,
  coaches,
  measurements
})
