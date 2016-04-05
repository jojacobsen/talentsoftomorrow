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
        <div className='row'>
          {this.props.measurements.map((measurement, index) =>
            <div key={measurement.id} className='col-sm-3'>
              <MeasurementListItem {...measurement} />
            </div>
          )}
        </div>
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
