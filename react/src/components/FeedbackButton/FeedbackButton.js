import React from 'react'

type Props = {
  defaultText: String,
  loadingText: String
};
export class FeedbackButton extends React.Component {
  props: Props;

  render () {
    return (
      <button type='submit' className={`btn-primary ${classes['form-element']}`}>
        Submit
      </button>
    )
  }
}

export default FeedbackButton

