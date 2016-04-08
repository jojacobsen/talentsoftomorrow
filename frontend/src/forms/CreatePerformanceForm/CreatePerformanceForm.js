import React from 'react'
import { reduxForm } from 'redux-form'
import TextInput from 'components/InputFields/TextInput'
import classNames from 'classnames'
import classes from './style.scss'
import CommentModal from './CommentModal'

const fields = ['score', 'description', 'player']

const validate = (values) => {
  const errors = {}
  return errors
}

// const hasErrors = (errors) => {
//   return Object.keys(errors).length
// }

const playerName = (player) => {
  return `${player.value.user.first_name} ${player.value.user.last_name}`
}

type Props = {
  handleSubmit: Function,
  fields: Object,
  performance: Object,
  label: String
};

class CreatePerformanceForm extends React.Component {
  props: Props;

  constructor () {
    super()
    this.clickIcon = this.clickIcon.bind(this)
    this.checkPerformanceState = this.checkPerformanceState.bind(this)
    this.state = {
      hideDescription: true
    }
  }

  clickIcon () {
    this.setState({ hideDescription: !this.state.hideDescription })
  }

  checkPerformanceState () {
    if (this.props.performance.value) {
      return true
    }
  }

  componentDidMount () {
    this.checkPerformanceState()
  }

  componentWillReceiveProps () {
    this.checkPerformanceState()
  }

  render () {
    const { fields: { score, description, player }, handleSubmit } = this.props

    let descriptionClass = classNames({
      'hidden': this.state.hideDescription
    })

    let inputNewClass = classNames({
      'hidden': this.checkPerformanceState()
    })

    let scoreSavedClass = classNames({
      'hidden': !this.checkPerformanceState()
    })

    return (
      <form onSumbit={handleSubmit}>
        <div className='row relative'>
          <div className='col-md-4'>
            <div className={classes['player-name']}>
              {player.value && playerName(player)}
            </div>
          </div>

          <div className={inputNewClass}>
            <div className='col-xs-7 col-md-5'>
              <TextInput label={this.props.label} {...score}/>
            </div>

            <div className={descriptionClass}>
              <CommentModal
                playerName={player.value && playerName(player)}
                clickIcon={this.clickIcon} {...description} />
            </div>

            <div className='col-xs-5 col-md-2'>
              <button className='btn-primary' type='submit' onClick={handleSubmit}>
                Gem
              </button>
            </div>

            <div className='col-md-1'>
              <div className={classes['comment-icon']} onClick={this.clickIcon}>
                <div className='oi' data-glyph='comment-square'></div>
              </div>
            </div>
          </div>

          <div className={scoreSavedClass}>
            <div className='col-md-8'>
              <div className={classes['performance-result']}>
                {this.props.performance.value}
              </div>
            </div>
          </div>
        </div>
      </form>
    )
  }
}

export default reduxForm({
  form: 'CreatePerformanceForm',
  fields,
  validate
})(CreatePerformanceForm)
