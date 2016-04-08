import React from 'react'
import { connect } from 'react-redux'
import { loadMeasurements } from '../../redux/modules/measurements'
import MeasurementListItem from 'components/MeasurementListItem/MeasurementListItem'

type Props = {
  loadMeasurements: Function,
  measurements: Array
};

export class Measurements extends React.Component {
  props: Props;

  componentDidMount () {
    this.props.loadMeasurements()
  }

  render () {
    return (
      <div>
        <h1>Measurements</h1>
        <ul className='list'>
          {this.props.measurements.map((measurement, index) =>
            <MeasurementListItem key={measurement.id} {...measurement} />
          )}
        </ul>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    measurements: state.measurements
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    loadMeasurements: () => {
      dispatch(loadMeasurements())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Measurements)
