import React from 'react'

type Props = {
  buttonText: String
};
export class FeedbackButton extends React.Component {
  props: Props;

  render () {
    return (
      <button type='submit' className='btn-primary full-width'>
        {this.props.buttonText}
      </button>
    )
  }
}

export default FeedbackButton
