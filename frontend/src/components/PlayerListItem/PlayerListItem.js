import React from 'react'

type Props = {
  first_name: String,
  last_name: String,
  username: String
};

export class PlayerListItem extends React.Component {
  props: Props;

  render () {
    return (
      <li className='list-item'>
        <div className='row'>
          <div className='col-sm-2'>
            <div className='list-header-mobile'>
              Username
            </div>

            <div className='list-item-text'>
              {this.props.username}
            </div>
          </div>
          <div className='col-sm-2'>
            <div className='list-header-mobile'>
              Full name
            </div>

            <div className='list-item-text last'>
              {this.props.first_name || 'Lionel'}
              {" "}
              {this.props.last_name || 'Messi'}
            </div>
          </div>
        </div>
      </li>
    )
  }
}

export default PlayerListItem
