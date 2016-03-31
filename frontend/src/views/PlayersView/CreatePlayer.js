import React from 'react'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'
import { connect } from 'react-redux'
import { reduxForm } from 'redux-form'
import { createPlayer } from '../../redux/modules/players'

export const fields = ['first_name', 'last_name', 'birthday', 'gender']

const validate = (values) => {
  const errors = {}
  return errors
}

type Props = {
  fields: Array,
  handleSubmit: Function
};

export class CreatePlayer extends React.Component {
  props: Props;

  constructor () {
    super()
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit (event) {
    event.preventDefault()

    this.props.dispatch(createPlayer())
  }

  render () {
    const {fields: {first_name, last_name, birthday, gender}, handleSubmit} = this.props

    return (
      <div>
        <SubPageHeader path='/talents' title='Add talent'/>

        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label className='form-label'>First Name</label>
            <input className='form-input' type='text' placeholder='First Name' {...first_name}/>
          </div>
          <div className='form-group'>
            <label className='form-label'>Last Name</label>
            <input className='form-input' type='text' placeholder='Last Name' {...last_name}/>
          </div>
          <div className='form-group'>
            <label className='form-label'>Birthday</label>
            <input className='form-input' type='text' placeholder='Birthday' {...birthday}/>
          </div>
          <div className='form-group'>
            <label className='form-label'>Gender</label>
            <input className='form-input' type='text' placeholder='Gender' {...gender}/>
          </div>
          <button className='btn-primary' type='submit'>Save</button>
        </form>
      </div>
    )
  }
}

let CreatePlayerForm = reduxForm({
  form: 'createPlayer',
  fields,
  validate
})(CreatePlayer)

export default connect()(CreatePlayerForm);
