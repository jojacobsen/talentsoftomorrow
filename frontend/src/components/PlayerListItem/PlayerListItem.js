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
          <div className='col-sm-3'>
            <div className='list-header-mobile'>
              Navn
            </div>

            <div className='list-item-text'>
              {this.props.user.first_name || 'Lionel'}
              {" "}
              {this.props.user.last_name || 'Messi'}
            </div>
          </div>

          <div className='col-sm-2'>
            <div className='list-header-mobile'>
              Fødselsdag
            </div>

            <div className='list-item-text'>
              {this.props.birthday}
            </div>
          </div>

          <div className='col-sm-7'>
            <div className='list-header-mobile'>
              Laboratorie-ID
            </div>

            <div className='list-item-text last'>
              {this.props.lab_key}
            </div>
          </div>
        </div>
      </li>
    )
  }
}

export default PlayerListItem
