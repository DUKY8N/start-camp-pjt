export async function handler(event) {
  const path = event.path?.replace(/^\/\.netlify\/functions\/tour-proxy/, '') || ''
  const targetPath = path || '/'
  const serviceKey = process.env.VITE_TOUR_API_KEY || process.env.TOUR_API_KEY

  if (!serviceKey) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ error: 'Tour API key is not configured.' }),
    }
  }

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
      },
      body: '',
    }
  }

  const url = new URL(`https://apis.data.go.kr/B551011/KorService2${targetPath}`)

  const queryParams = new URLSearchParams(event.queryStringParameters || {})
  if (!queryParams.has('serviceKey')) {
    queryParams.set('serviceKey', serviceKey)
  }

  url.search = queryParams.toString()

  const response = await fetch(url.toString(), {
    headers: {
      Accept: 'application/json',
    },
  })

  const text = await response.text()

  return {
    statusCode: response.status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
    body: text,
  }
}
