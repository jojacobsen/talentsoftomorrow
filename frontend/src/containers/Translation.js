import React from 'react'
import { connect } from 'react-redux'
import { loadTranslations } from '../redux/modules/translations'

type Props = {
  translations: Object,
  loadTranslations: Function,
  group: String,
  handle: String
};
export class Translation extends React.Component {
  props: Props;

  constructor () {
    super()
    this.getTranslation = this.getTranslation.bind(this)
  }

  componentDidMount () {
    if (Object.keys(this.props.translations).length === 0) {
      this.props.loadTranslations()
    }
  }

  getTranslation () {
    if (Object.keys(this.props.translations).length && this.props.group && this.props.handle) {
      return this.props.translations[this.props.group][this.props.handle]
    } else {
      return 'Translation missing'
    }
  }

  render () {
    return (
      <div>
        {this.getTranslation()}
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    translations: state.translations
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
    loadTranslations: () => {
      dispatch(loadTranslations())
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Translation)
