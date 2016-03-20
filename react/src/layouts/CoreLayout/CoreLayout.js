import React, { PropTypes } from 'react'
import '../../styles/core.scss'
import { Link } from 'react-router'

export class CoreLayout extends React.Component {
  static propTypes = {
    children: PropTypes.element
  }

  render () {
    return (
      <div>
        <nav className='navigation'>
          <div className='nav-user'>
            <div className='nav-user-image'>
              <img src='/images/trainer.jpg' />
            </div>

            <div className='nav-user-name'>
              Jürgen
            </div>
          </div>

          <Link to='/dashboard' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='dashboard'></span>
            Dashboard
          </Link>

          <Link to='/talents' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='people'></span>
            Talenter
          </Link>

          <Link to='/compare' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='random'></span>
            Sammenlign
          </Link>

          <Link to='/measure' className='nav-item' activeClassName='active'>
            <span className='oi nav-item-icon' data-glyph='timer'></span>
            Tests
          </Link>
        </nav>

        <div className='content-wrapper'>
          {this.props.children}
        </div>
      </div>
    )
  }
}

export default CoreLayout
