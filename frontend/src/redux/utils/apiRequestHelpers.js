export function getHeader (token) {
  return {
    mode: 'cors',
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `JWT ${token}`
    }
  }
}

export function postHeader (token, json) {
  return {
    mode: 'cors',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `JWT ${token}`
    },
    body: JSON.stringify(json)
  }
}

export function apiBase () {
  if (__DEV__) return 'http://127.0.0.1:8000'
  if (__PROD__) return 'http://INSERT-BASE-API-URL.com'
}
