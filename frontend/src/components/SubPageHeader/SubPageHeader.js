import React from 'react'
import { Link } from 'react-router'
import classes from './style.scss'

type Props = {
  title: String,
  path: String
};
export class SubPageHeader extends React.Component {
  props: Props;

  render () {
    return (
      <div className={classes['wrapper']}>
        <div className='row'>
          <div className='col-sm-1 col-xs-2'>
            <Link to={this.props.path} className={classes['back-arrow']}>
              <span className='oi' data-glyph='chevron-left'></span>
            </Link>
          </div>
          <div className='col-sm-11 col-xs-10'>
            <h1>{this.props.title}</h1>
          </div>
        </div>
      </div>
    )
  }
}

export default SubPageHeader
