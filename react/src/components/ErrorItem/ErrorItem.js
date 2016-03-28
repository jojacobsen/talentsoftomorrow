import React from 'react'
import classes from './ErrorItem.scss'

type Props = {
  errorItem: String
};
export class ErrorItem extends React.Component {
  props: Props;

  render () {
    return (
      <li className={classes['list-item']}>{this.props.errorItem}</li>
    )
  }
}

export default ErrorItem

