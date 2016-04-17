// TODO: consider better solution as translation object
// might be imported without ever being used
// const defaultLanguage = require('../../locales/en')
// const initialState = defaultLanguage.translations
const initialState = {}


/* ================= */
/* === Actions ===== */
/* ================= */

export const translationsLoaded = (json) => {
  return {
    type: 'TRANSLATIONS_LOADED',
    translations: json.translations
  }
}

/* ================= */
/* === Thunks ====== */
/* ================= */

export function loadTranslations (locale) {
  // TODO: Set/pass locale dynamically

  return function (dispatch) {
    let json = require('../../locales/en')

    dispatch(translationsLoaded(json))

  }
}

/* ================= */
/* === Reducer ===== */
/* ================= */

function translations (state = initialState, action) {
  switch (action.type) {
    case 'TRANSLATIONS_LOADED':
      return action.translations
    default:
      return state
  }
}

export default translations
