import React from 'react'
import { reduxForm } from 'redux-form'

export const fields = [first_name, last_name, birthday, gender]

const validate = (values) => {
  const errors = {}
  return errors
}

type Props = {
  handleSubmit: Function,
  fields: Object,
}
export class CreatePlayer extends React.Component {
  props: Props;

  defaultProps = {
    fields: {},
  }

  render() {
    const { fields, handleSubmit } = this.props

    return (
      <form onSubmit={handleSubmit}>
          <div>
            <label>First Name</label>
            <input type='text' placeholder='First Name' {...first_name}/>
          </div>
          <div>
            <label>Last Name</label>
            <input type='text' placeholder='Last Name' {...last_name}/>
          </div>
          <div>
            <label>Birthday</label>
            <input type='text' placeholder='Birthday' {...birthday}/>
          </div>
          <div>
            <label>Gender</label>
            <input type='text' placeholder='Gender' {...gender}/>
          </div>
          <button type='submit'>Submit</button>
      </form>
    )
  }
}

CreatePlayer = reduxForm({
  form: 'CreatePlayer',
  fields,
  validate
})(CreatePlayer)

export default CreatePlayer
