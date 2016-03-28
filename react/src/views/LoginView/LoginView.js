import React from 'react'
import { connect } from 'react-redux'
import { tryLogin } from '../../redux/modules/auth'
import ErrorItem from 'components/ErrorItem/ErrorItem'
import FeedbackButton from 'components/FeedbackButton/FeedbackButton'
import classes from './LoginView.scss'

type Props = {
  onClick: Function,
  username: String,
  errors: Array,
  loggedIn: Boolean
};

export class Login extends React.Component {
  props: Props

  constructor () {
    super()
    this.storeFormData = this.storeFormData.bind(this)
    this.buttonText = this.buttonText.bind(this)
  }

  storeFormData (event) {
    event.preventDefault()

    let formData = {
      username: this.refs.username.value,
      password: this.refs.password.value
    }

    this.props.onClick(formData)
  }

  buttonText () {
    if(this.props.isRequesting) {
      return 'Loading...'
    } else {
      return 'Login'
    }
  }

  render () {
    return (
      <div className={`container ${classes.container}`} >
        <div className='col-md-offset-3 col-md-6'>
          <p className={classes.welcome}>
            Welcome at Talents of Tomorrow
          </p>
          <h1>Please sign in</h1>
          <form onSubmit={this.storeFormData}>
            <input
              ref='username'
              type='text'
              placeholder='username'
              className={`form-input ${classes['form-element']}`} />

            <input
              ref='password'
              type='password'
              placeholder='password'
              className={`form-input ${classes['form-element']}`} />

            <FeedbackButton buttonText={this.buttonText()} />
          </form>

          <ul>
            {this.props.errors.map((errorItem, index) =>
              <ErrorItem key={index} errorItem={errorItem} />
            )}
          </ul>
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  console.log(state.auth.userInfo.errors)
  return {
    username: state.auth.userInfo.username,
    errors: state.auth.userInfo.errors,
    loggedIn: state.auth.userInfo.loggedIn,
    isRequesting: state.auth.userInfo.isRequesting
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    onClick: (formData) => {
      dispatch(tryLogin(formData))
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Login)
