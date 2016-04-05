import React, { PropTypes } from 'react'
import '../../styles/core.scss'
import { Link } from 'react-router'
import { connect } from 'react-redux'
import { logout, authInit } from '../../redux/modules/auth'
import Alert from 'react-s-alert'
import 'react-s-alert/dist/s-alert-default.css'
import 'react-s-alert/dist/s-alert-css-effects/jelly.css'

type Props = {
  logout: Function,
  authInit: Function,
  username: String,
  children: PropTypes.element
};

export class CoreLayout extends React.Component {
  props: Props

  constructor () {
    super()
    this.logout = this.logout.bind(this)
  }

  componentDidMount () {
    this.props.authInit()
  }

  logout () {
    this.props.logout()
  }

  render () {
    return (
      <div>
        <nav className='navigation'>
          <div className='nav-user'>
            <div className='oi nav-logout' data-glyph='account-logout' onClick={this.logout}></div>

            <div className='nav-user-image'>
              <img src='/images/trainer.jpg' />
            </div>

            <div className='nav-user-name'>
              {this.props.username}
            </div>
          </div>

          <Link to='/dashboard' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='dashboard'></span>
            <span className='nav-item-text'>Dashboard</span>
          </Link>

          <Link to='/talents' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='people'></span>
            <span className='nav-item-text'>Talenter</span>
          </Link>

          <Link to='/compare' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='random'></span>
            <span className='nav-item-text'>Sammenlign</span>
          </Link>

          <Link to='/measurements' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='timer'></span>
            <span className='nav-item-text'>Tests</span>
          </Link>

          <Link to='/settings' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='cog'></span>
            <span className='nav-item-text'>Indstillinger</span>
          </Link>
        </nav>

        <div className='content-wrapper'>
          {this.props.children}
        </div>

        <Alert
          stack={{limit: 3}}
          timeout={8000}
          position='bottom-right'
          effect='jelly'
          html={false} />
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    username: state.auth.userInfo.username
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    logout: () => {
      dispatch(logout())
    },
    authInit: () => {
      dispatch(authInit())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(CoreLayout)
