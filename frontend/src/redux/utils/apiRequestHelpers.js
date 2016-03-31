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

export function apiBase () {
  if (__DEV__) return 'http://127.0.0.1:8000'
  if (__PROD__) return 'http://INSERT-BASE-API-URL.com'
}