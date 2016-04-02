export function convertObjectToText (obj) {
  var prop
  var string = []

  if (typeof (obj) === 'object' && (obj.join === undefined)) {
    string.push(' ')
    for (prop in obj) {
      string.push(prop, ': ', convertObjectToText(obj[prop]))
    };
    string.push(' ')

  // is array
  } else if (typeof (obj) === 'object' && !(obj.join === undefined)) {
    string.push(' ')
    for (prop in obj) {
      string.push(convertObjectToText(obj[prop]))
    }
    string.push(' ')

  // is function
  } else if (typeof (obj) === 'function') {
    string.push(obj.toString())

  // all other values can be done with JSON.stringify
  } else {
    string.push(JSON.stringify(obj))
  }

  return string.join('')
}
