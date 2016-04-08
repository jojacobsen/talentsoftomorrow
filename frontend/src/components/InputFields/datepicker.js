import React from 'react'

type Props = {
  value: Object,
  label: String,
  touched: Boolean,
  error: String
};

export class Datepicker extends React.Component {
  props: Props;

  render () {
    return (
      <div className='form-group'>
        <label className='form-label'>{this.props.label}</label>
        <input className='form-input' type='date' placeholder='Fornavn' {...this.props}/>
        {this.props.touched && this.props.error && <div className='form-error'>{this.props.error}</div>}
      </div>
    )
  }
}

export default Datepicker