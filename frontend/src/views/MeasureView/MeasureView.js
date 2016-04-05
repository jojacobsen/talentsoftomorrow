import React from 'react'
import { connect } from 'react-redux'
import { loadMeasurements } from '../../redux/modules/measurements'

type Props = {

};
export class Measure extends React.Component {
  props: Props;

  render () {
    console.log(this.props.measurements)
    return (
      <h1>Tests</h1>
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
    loadPlayers: () => {
      dispatch(loadMeasurements())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Measure)
