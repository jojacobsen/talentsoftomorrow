import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'
import auth from './modules/auth'
import players from './modules/players'

export default combineReducers({
  router,
  auth,
  players
})
