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
    const { fields: { score, description, player }, handleSubmit } = this.props

    let descriptionClass = classNames({
      'hidden': this.state.hideDescription
    })

    return (
      <form onSumbit={handleSubmit}>
        <div className='row relative'>
          <div className='col-xs-7 col-md-9'>
            <TextInput label={this.props.label} {...score}/>
          </div>

          <div className={descriptionClass}>
            <CommentModal clickIcon={this.clickCommentBtn} {...description} />
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
      </form>
    )
  }
}

export default reduxForm({
  form: 'CreatePerformanceForm',
  fields,
  validate
})(CreatePerformanceForm)
