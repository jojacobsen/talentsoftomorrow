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
    console.log(this.props.players)
    return (
      <div>
        <h1>Talenter</h1>
        <ul className='list'>
          {this.props.players.map((player, index) =>
            <PlayerListItem key={player.id} {...player} />
          )}
        </ul>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    players: state.players.players
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
