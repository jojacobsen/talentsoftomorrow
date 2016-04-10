import React from 'react'
import classes from './style.scss'

type Props = {
};

class ShowPerformance extends React.Component {
  props: Props;

  render () {
    return (
      <div className='row'>
        <div className='col-md-8'>
          <div className={classes['performance-result']}>
            {this.props.performance.value}
          </div>
        </div>

        <div className='col-md-2'>
          Edit
        </div>

        <div
          className='col-md-2'
          data-performance-id={this.props.performance.id}
          onClick={this.props.handleAddClick}>
          Add
        </div>
      </div>
    )
  }
}

export default ShowPerformance
