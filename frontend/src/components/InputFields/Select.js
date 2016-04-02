import React from 'react'

type Props = {
  value: Object,
  label: String,
  touched: Boolean,
  error: String,
  options: Array
};

export class Select extends React.Component {
  props: Props;

  render () {
    return (
      <div className='form-group'>
        <label className='form-label'>{this.props.label}</label>
        <select value={this.props.value || 'default'} className='form-select' {...this.props}>
          {this.props.options.map((option) =>
            <option key={option.value} value={option.value}>
              {option.name}
            </option>
          )}
        </select>
        {this.props.touched && this.props.error && <div className='form-error'>{this.props.error}</div>}
      </div>
    )
  }
}

export default Select
