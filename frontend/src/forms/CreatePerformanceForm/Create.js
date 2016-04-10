import React from 'react'
import { reduxForm } from 'redux-form'
import TextInput from 'components/InputFields/TextInput'
import classNames from 'classnames'
import classes from './style.scss'
import CommentModal from './CommentModal'

const fields = ['score', 'description', 'player', 'upper_limit', 'lower_limit']

const validate = (values) => {
  const errors = {}

  let score = values.score || 0

  if (! /^[0-9.]+$/.test(score)) { // TODO: Use regex instead
    errors.score = 'Skal være et tal'
  }

  if (String(score).indexOf(',') > 0) {
    errors.score = 'Separer venligst med punktum'
  }

  if (score > parseFloat(values.upper_limit)) {
    errors.score = `Tallet er for højt. Max ${parseInt(values.upper_limit)}`
  }

  if (score < parseFloat(values.lower_limit)) {
    errors.score = `Tallet er for lavt (Min. ${parseInt(values.lower_limit)})`
  }

  if (score === 0) {
    errors.score = 'Udfyld venligst'
  }

  return errors
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
    this.state = {
      hideDescription: true
    }
  }

  clickCommentBtn () {
    this.setState({ hideDescription: !this.state.hideDescription })
  }

  render () {
    const { fields: { score, description, player, upper_limit, lower_limit }, handleSubmit } = this.props

    let descriptionClass = classNames({
      'hidden': this.state.hideDescription
    })

    return (
      <form onSumbit={handleSubmit} data-passive-vars={player + upper_limit + lower_limit}>
        <div className='row relative'>
          <div className='col-xs-12 col-sm-7'>
            <TextInput label={this.props.measurement.unit} {...score}/>
          </div>

          <div className='col-xs-12 col-sm-4'>
            <button className='btn-primary' type='submit' onClick={handleSubmit}>
              Gem
            </button>
          </div>

          <div className='col-sm-1'>
            <div className={classes['comment-icon']} onClick={this.clickCommentBtn}>
              <div className='oi' data-glyph='comment-square'></div>
            </div>
          </div>
        </div>

        <div className={descriptionClass}>
          <CommentModal clickIcon={this.clickCommentBtn} {...description} />
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
