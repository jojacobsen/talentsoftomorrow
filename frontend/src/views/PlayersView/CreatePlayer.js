import React from 'react'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'
import { connect } from 'react-redux'
import { reduxForm } from 'redux-form'
import { createPlayer } from '../../redux/modules/players'

export const fields = ['first_name', 'last_name', 'birthday', 'gender', 'coaches']

const validate = (values) => {
  const errors = {}
  return errors
}

type Props = {
  fields: Array,
  handleSubmit: Function,
  dispatch: Function
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
    const {fields: {first_name, last_name, birthday, gender, coaches}} = this.props

    return (
      <div>
        <SubPageHeader path='/talents' title='Add talent'/>

        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label className='form-label'>Fornavn</label>
            <input className='form-input' type='text' placeholder='Fornavn' {...first_name}/>
          </div>
          <div className='form-group'>
            <label className='form-label'>Efternavn</label>
            <input className='form-input' type='text' placeholder='Efternavn' {...last_name}/>
          </div>
          <div className='form-group'>
            <label className='form-label'>Køn</label>
            <select value={gender.value || 'default'} className='form-select' {...gender}>
              <option value='default' disabled>Køn</option>
              <option value='M'>Mand</option>
              <option value='F'>Kvinde</option>
            </select>
          </div>
          <div className='form-group'>
            <label className='form-label'>Coaches</label>
            <select value={coaches.value || 'default'} className='form-select' {...coaches}>
              <option value='default' disabled>Spillerens træner</option>
              <option value='1'>Pep</option>
              <option value='1'>Ståle</option>
            </select>
          </div>
          <div className='form-group'>
            <label className='form-label'>Fødselsdag</label>
            <input className='form-input' type='date' placeholder='Fødselsdag' {...birthday}/>
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

export default connect()(CreatePlayerForm)
