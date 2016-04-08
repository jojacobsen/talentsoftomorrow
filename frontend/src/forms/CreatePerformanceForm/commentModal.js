import React from 'react'
import classes from './style.scss'
import TextArea from 'components/InputFields/TextArea'

type Props = {
  errorItem: String,
  playerName: String,
  clickIcon: Function,
  description: Object
};
export class CommentModal extends React.Component {
  props: Props;

  clickIcon () {
    this.setState({ hideDescription: !this.state.hideDescription })
  }

  render () {
    return (
      <div className={classes['description-modal']}>
        <div className='container'>
          <h2>Kommentar (valgfri)</h2>
          <p>
            {`Tilføj kommentar til målingen af ${this.props.playerName}
              om særlige forhold, der kan have
              haft særlig indflydelse på resultatet`}
          </p>

          <div className={`oi ${classes['close-icon']}`} data-glyph='x' onClick={this.props.clickIcon}></div>
          <TextArea label='Kommentar' {...this.props.description}/>
          <div className='btn-secondary' onClick={this.props.clickIcon}>
            Ok
          </div>
        </div>
      </div>
    )
  }
}

export default CommentModal

