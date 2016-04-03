import React from 'react'
import { SubPageHeader } from 'components/SubPageHeader/SubPageHeader'
import TextInput from 'components/InputFields/TextInput'
import Select from 'components/InputFields/Select'
import Datepicker from 'components/InputFields/Datepicker'
import { connect } from 'react-redux'
import { reduxForm } from 'redux-form'
import { createPlayer } from '../../redux/modules/players'
import { loadCoaches } from '../../redux/modules/coaches'

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
    this.options = this.options.bind(this)
  }

  componentDidMount () {
    this.props.dispatch(loadCoaches())
  }

  handleSubmit (event) {
    event.preventDefault()

    if (!hasErrors(this.props.errors)) {
      this.props.dispatch(createPlayer())
    }
  }

  options () {
    let coaches = []

    for (let coach of this.props.coaches) {
      coaches.push({
        value: coach.id,
        name: `${coach.user.first_name} ${coach.user.last_name}`
      })
    }

    return coaches
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
            options={this.options()}
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
  form: 'CreatePlayer',
  fields,
  validate
},
(state) => ({ // mapStateToProps
  coaches: state.coaches // will pull state into form's initialValues
}))(CreatePlayer)

export default connect()(CreatePlayerForm)
