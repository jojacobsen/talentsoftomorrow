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
    this.clickCommentBtn = this.clickCommentBtn.bind(this)
    this.clickAddBtn = this.clickAddBtn.bind(this)
    this.checkPerformanceState = this.checkPerformanceState.bind(this)
    this.state = {
      hideDescription: true,
      hideSavedScore: true
    }
  }

  clickCommentBtn () {
    this.setState({ hideDescription: !this.state.hideDescription })
  }

  clickAddBtn () {
    this.setState({ hideSavedScore: false })
  }

  checkPerformanceState () {
    if (this.props.performance.value && this.state.hideSavedScore) {
      return true
    } else {
      return false
    }
  }

  // componentDidMount () {
  //   this.checkPerformanceState()
  // }

  // componentWillReceiveProps () {
  //   this.checkPerformanceState()
  // }

  render () {
    const { fields: { score, description, player }, handleSubmit } = this.props

    let descriptionClass = classNames({
      'hidden': this.state.hideDescription
    })

    let inputNewClass = classNames({
      'hidden': this.checkPerformanceState()
    })

    let savedScoreClass = classNames({
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
                clickIcon={this.clickCommentBtn} {...description} />
            </div>

            <div className='col-xs-5 col-md-2'>
              <button className='btn-primary' type='submit' onClick={handleSubmit}>
                Gem
              </button>
            </div>

            <div className='col-md-1'>
              <div className={classes['comment-icon']} onClick={this.clickCommentBtn}>
                <div className='oi' data-glyph='comment-square'></div>
              </div>
            </div>
          </div>

          <div className={savedScoreClass}>
            <div className='col-md-8'>
              <div className='col-md-8'>
                <div className={classes['performance-result']}>
                  {this.props.performance.value}
                </div>
              </div>
              <div className='col-md-2'>
                Edit
              </div>
              <div className='col-md-2' onClick={this.clickAddBtn}>
                Add
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
