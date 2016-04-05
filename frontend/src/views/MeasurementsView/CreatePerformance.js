import React from 'react'
import { connect } from 'react-redux'
import { loadMeasurements } from '../../redux/modules/measurements'
import { loadPlayers } from '../../redux/modules/players'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'

type Props = {
  measurements: Array,
  players: Array,
  loadPlayers: Function,
  loadMeasurements: Function,
  routeParams: Object
};

export class CreatePerformance extends React.Component {
  props: Props;

  constructor () {
    super()
    this.getMeasurement = this.getMeasurement.bind(this)
  }

  componentDidMount () {
    if (this.props.measurements.length === 0) {
      this.props.loadMeasurements()
    }

    if (this.props.players.length === 0) {
      this.props.loadPlayers()
    }
  }

  getMeasurement () {
    let measurementId = parseInt(this.props.routeParams.measurementId)

    return this.props.measurements.find((measurement) => measurement.id === measurementId) || {}
  }

  render () {
    console.log(this.props.players)
    return (
      <div>
        <SubPageHeader path='/measurements' title={this.getMeasurement().name} />

        <ul className='list'>
          {this.props.players.map((player, index) =>
            <p key={player.id}>
              {player.user.first_name}
              {' '}
              {player.user.last_name}
            </p>
          )}
        </ul>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    measurements: state.measurements,
    players: state.players
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    loadMeasurements: () => {
      dispatch(loadMeasurements())
    },
    loadPlayers: () => {
      dispatch(loadPlayers())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(CreatePerformance)
