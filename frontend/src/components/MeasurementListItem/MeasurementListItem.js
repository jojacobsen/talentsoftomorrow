import React from 'react'
import { Link } from 'react-router'
import classes from './style.scss'

type Props = {
  description: String,
  id: Number,
  lower_limit: Number,
  upper_limit: Number,
  name: String,
  unit: String
};

const iconClassName = (name) => {
  return 'icon-' + name.toLowerCase().replace(/ /g, '-')
}

// TODO: add icons in stylesheet
export class MeasurementListItem extends React.Component {
  props: Props;

  render () {
    return (
      <Link to={`/measurements/create/${this.props.id}`} className={classes['list-item']}>
        <div className={classes['icon']}>
          <div className={iconClassName(this.props.name)}></div>
        </div>

        <div className={classes['text']}>
          {this.props.name}
        </div>
      </Link>
    )
  }
}

export default MeasurementListItem

