import React from 'react'
import { connect } from 'react-redux'
import { loadMeasurements } from '../../redux/modules/measurements'
import { createPerformance, loadPerformances } from '../../redux/modules/performances'
import { loadPlayers } from '../../redux/modules/players'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'
import CreatePerformanceForm from 'forms/CreatePerformanceForm/CreatePerformanceForm'
import classes from './style.scss'

type Props = {
  measurements: Array,
  players: Array,
  performances: Array,
  loadPlayers: Function,
  loadMeasurements: Function,
  loadPerformances: Function,
  createPerformance: Function,
  routeParams: Object
};

const initialValues = (player) => {
  return {
    player: player
  }
}

export class CreatePerformance extends React.Component {
  props: Props;

  constructor () {
    super()
    this.getMeasurement = this.getMeasurement.bind(this)
    this.getPerformance = this.getPerformance.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  componentDidMount () {
    if (this.props.measurements.length === 0) {
      this.props.loadMeasurements()
    }

    if (this.props.players.length === 0) {
      this.props.loadPlayers()
    }

    if (this.props.performances.length === 0) {
      this.props.loadPerformances()
    }
  }

  getMeasurement () {
    let measurementId = parseInt(this.props.routeParams.measurementId)

    return this.props.measurements.find((measurement) => measurement.id === measurementId) || {}
  }

  getPerformance (player) {
    let measurementId = this.getMeasurement().id

    return this.props.performances.find((item) => {
      return (item.measurement === measurementId && item.player === player.id)
    }) || {}
  }

  handleSubmit (formData) {
    let currentData = {
      measurement: this.getMeasurement(),
      player: formData.player
    }

    this.props.createPerformance(currentData)
  }

  render () {
    return (
      <div>
        <SubPageHeader path='/measurements' title={this.getMeasurement().name} />
        <div >
          {this.props.players.map((player, index) =>
            <div className={`row ${classes['item-row']}`} key={player.id}>
              <div className='col-xs-12'>
                <CreatePerformanceForm
                  label={this.getMeasurement().unit}
                  performance={this.getPerformance(player)}
                  initialValues={initialValues(player)}
                  formKey={player.id.toString()}
                  onSubmit={this.handleSubmit}/>
              </div>
            </div>
          )}
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    measurements: state.measurements,
    players: state.players,
    performances: state.performances
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    loadMeasurements: () => {
      dispatch(loadMeasurements())
    },
    createPerformance: (currentData) => {
      dispatch(createPerformance(currentData))
    },
    loadPlayers: () => {
      dispatch(loadPlayers())
    },
    loadPerformances: () => {
      dispatch(loadPerformances())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(CreatePerformance)
