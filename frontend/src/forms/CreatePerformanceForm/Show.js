import React from 'react'
import classes from './style.scss'

type Props = {
  performance: Object,
  handleAddClick: Function
};

const formatResult = (value) => {
  return parseInt(value).toFixed(2)
}

class ShowPerformance extends React.Component {
  props: Props;

  render () {
    return (
      <div className='row'>
        <div className='col-xs-7'>
          <div className={classes['performance-result']}>
            {formatResult(this.props.performance.value)}

            <span className={classes['performance-unit']}>
              {this.props.unit}
            </span>
          </div>
        </div>

        <div className='col-xs-2 col-sm-1'>
          <div className='btn-round'>
            <div className='oi' data-glyph='pencil'></div>
          </div>
        </div>

        <div className='col-xs-2 col-sm-1'>
          <div
            className='btn-round'
            data-performance-id={this.props.performance.id}
            onClick={this.props.handleAddClick}>
              <div className='oi' data-glyph='plus'></div>
          </div>
        </div>
      </div>
    )
  }
}

export default ShowPerformance
