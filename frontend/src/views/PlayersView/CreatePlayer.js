import React from 'react'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'
import TextInput from 'components/InputFields/TextInput'
import Select from 'components/InputFields/Select'
import Datepicker from 'components/InputFields/Datepicker'
import { connect } from 'react-redux'
import { reduxForm } from 'redux-form'
import { createPlayer } from '../../redux/modules/players'

export const fields = ['first_name', 'last_name', 'birthday', 'gender', 'coaches']

const validate = (values) => {
  const errors = {}
  if (!values.first_name) {
    errors.first_name = 'Skal udfyldes'
  }

  if (!values.last_name) {
    errors.last_name = 'Skal udfyldes'
  }

  if (!values.gender) {
    errors.gender = 'Skal udfyldes'
  }

  if (!values.birthday) {
    errors.birthday = 'Skal udfyldes'
  }

  return errors
}

const hasErrors = (errors) => {
  return Object.keys(errors).length
}

type Props = {
  fields: Array,
  handleSubmit: Function,
  dispatch: Function,
  errors: Object
};

export class CreatePlayer extends React.Component {
  props: Props;

  constructor () {
    super()
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit (event) {
    event.preventDefault()

    if (!hasErrors(this.props.errors)) {
      this.props.dispatch(createPlayer())
    }
  }

  render () {
    const {fields: {first_name, last_name, birthday, gender, coaches}} = this.props
    return (
      <div>
        <SubPageHeader path='/talents' title='Add talent'/>
        <form onSubmit={this.handleSubmit}>
          <TextInput label='Fornavn' {...first_name} />
          <TextInput label='Efternavn' {...last_name} />
          <Select label='Køn' options={[{ value: 'M', name: 'M' }, { value: 'F', name: 'K' }]} {...gender} />
          <Select
            label='Træner'
            options={[{ value: '1', name: 'Pep Guardiola' }, { value: '2', name: 'Ståle Solbakken' }]}
            {...coaches} />
          <Datepicker label='Fødselsdag' {...birthday} />
          <button className='btn-primary' disabled={hasErrors(this.props.errors)} type='submit'>
            Opret
          </button>
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
