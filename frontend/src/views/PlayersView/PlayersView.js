import React from 'react'
import { connect } from 'react-redux'
import { loadPlayers } from '../../redux/modules/players'
import PlayerListItem from 'components/PlayerListItem/PlayerListItem'
import { Link } from 'react-router'
import Translation from 'containers/Translation'

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
        <h1>
          <Translation group='players' handle='talents' />
        </h1>
        <div className='list-header-tablet'>
          <div className='row'>
            <div className='col-sm-3'>
              <Translation group='players' handle='name' />
            </div>
            <div className='col-sm-2'>
              <Translation group='players' handle='birthday' />
            </div>
            <div className='col-sm-3'>
              <Translation group='players' handle='lab_key' />
            </div>
          </div>
        </div>
        <div className='list-add-btn-wrapper'>
          <Link to='/talents/create'>
            <div className='list-add-btn'>
              <span className='oi' data-glyph='plus'></span>
            </div>
          </Link>
        </div>
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
