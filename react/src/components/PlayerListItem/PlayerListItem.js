import React from 'react'

type Props = {
  first_name: String,
  last_name: String
};
export class PlayerListItem extends React.Component {
  props: Props;

  render () {
    return (
      <li className='list-item'>
        <div className='row'>
          <div className='col-sm-2'>
            {this.props.first_name}
          </div>
          <div className='col-sm-2'>
            {this.props.last_name}
          </div>
        </div>
      </li>
    )
  }
}

export default PlayerListItem
