import React from 'react'
import { connect } from 'react-redux'
import { loadPlayers } from '../../redux/modules/players'
import PlayerListItem from 'components/PlayerListItem/PlayerListItem'

type Props = {
  loadPlayers: Function,
  players: Array
};

export class Players extends React.Component {
  props: Props;

  componentDidMount () {
    this.props.loadPlayers()
  }

  render () {
    return (
      <div>
        <h1>Talenter</h1>
        <div className='list-header-tablet'>
          <div className='row'>
            <div className='col-sm-2'>
              Username
            </div>
            <div className='col-sm-2'>
              Full name
            </div>
          </div>
        </div>
        <div className='list-add-btn-wrapper'>
          <div className='list-add-btn'>
            <span className='oi' data-glyph='plus'></span>
          </div>
        </div>
        <ul className='list'>
          {this.props.players.map((player, index) =>
            <PlayerListItem key={player.player_id} {...player.user} />
          )}
        </ul>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    players: state.players
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    loadPlayers: () => {
      dispatch(loadPlayers())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Players)
