import React from 'react'
import { Route, IndexRoute } from 'react-router'
import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import HomeView from 'views/HomeView/HomeView'
import Dashboard from 'views/DashboardView/DashboardView'
import Talents from 'views/TalentsView/TalentsView'
import Compare from 'views/CompareView/CompareView'
import Measure from 'views/MeasureView/MeasureView'

export default (store) => (
  <Route path='/' component={CoreLayout}>
    <IndexRoute component={HomeView} />
    <Route path='dashboard' component={Dashboard} />
    <Route path='talents' component={Talents} />
    <Route path='compare' component={Compare} />
    <Route path='measure' component={Measure} />
  </Route>
)
