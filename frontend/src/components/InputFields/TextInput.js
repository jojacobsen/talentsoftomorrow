import React from 'react'

type Props = {
  value: Object,
  label: String,
  touched: Boolean,
  error: String
};

export class TextInput extends React.Component {
  props: Props;

  render () {
    return (
      <div className='form-group'>
        <label className='form-label'>{this.props.label}</label>
        <input className='form-input' type='text' placeholder={this.props.label} {...this.props}/>
        {this.props.touched && this.props.error && <div className='form-error'>{this.props.error}</div>}
      </div>
    )
  }
}

export default TextInput
