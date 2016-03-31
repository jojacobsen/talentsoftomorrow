import React from 'react'
import { Route, IndexRoute } from 'react-router'

// components
import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import LoginView from 'views/LoginView/LoginView'
import Dashboard from 'views/DashboardView/DashboardView'
import Players from 'views/PlayersView/PlayersView'
import CreatePlayer from 'views/PlayersView/CreatePlayer'
import Compare from 'views/CompareView/CompareView'
import Measure from 'views/MeasureView/MeasureView'
import Settings from 'views/SettingsView/SettingsView'

function checkAuth (nextState, replace) {
  if (localStorage.getItem('user_token')) {
    replace({
      pathname: '/dashboard',
      state: { nextPathname: nextState.location.pathname }
    })
  }
}

// TODO: 404
export default (store) => (
  <Route path='/'>
    <Route path='/login' onEnter={checkAuth}>
      <IndexRoute component={LoginView} />
    </Route>

    <Route component={CoreLayout}>
      <Route path='dashboard' component={Dashboard} />
      <Route path='talents'>
        <IndexRoute component={Players} />
        <Route path='create' component={CreatePlayer} />
      </Route>
      <Route path='compare' component={Compare} />
      <Route path='measure' component={Measure} />
      <Route path='settings' component={Settings} />
    </Route>
  </Route>
)

