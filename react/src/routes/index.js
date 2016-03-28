import React from 'react'
import { Route, IndexRoute } from 'react-router'

// components
import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import LoginView from 'views/LoginView/LoginView'
import Dashboard from 'views/DashboardView/DashboardView'
import Talents from 'views/TalentsView/TalentsView'
import Compare from 'views/CompareView/CompareView'
import Measure from 'views/MeasureView/MeasureView'
import Settings from 'views/SettingsView/SettingsView'

var didRedirect = false

// TODO: move to a better place (currently pushstate ignores this. Also overwrites subpage routing on refresh)
function requireAuth (nextState, replace) {
  if (!didRedirect && !localStorage.getItem('user_token')) {
    didRedirect = true

    replace({
      pathname: '/login',
      state: { nextPathname: nextState.location.pathname }
    })
  } else if (!didRedirect) {
    didRedirect = true

    replace({
      pathname: '/dashboard',
      state: { nextPathname: nextState.location.pathname }
    })
  }
}

// TODO: 404
export default (store) => (
  <Route path='/' onEnter={requireAuth}>
    <Route path='/login'>
      <IndexRoute component={LoginView} />
    </Route>

    <Route component={CoreLayout}>
      <Route path='dashboard' component={Dashboard} />
      <Route path='talents' component={Talents} />
      <Route path='compare' component={Compare} />
      <Route path='measure' component={Measure} />
      <Route path='settings' component={Settings} />
    </Route>
  </Route>
)

