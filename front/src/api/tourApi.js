const isProduction = import.meta.env.PROD
const TOUR_API_BASE_URL = isProduction
  ? '/.netlify/functions/tour-proxy'
  : '/tour-api/B551011/KorService2'

const commonParams = {
  ...(isProduction ? {} : { serviceKey: import.meta.env.VITE_TOUR_API_KEY }),
  MobileOS: 'ETC',
  MobileApp: 'SeoulTravelCommunity',
  _type: 'json',
}

function getPayload(data) {
  const payload = data?.response ?? data
  const resultCode = payload?.header?.resultCode
  const resultMessage = payload?.header?.resultMsg

  if (resultCode && resultCode !== '0000') {
    throw new Error(resultMessage || `관광 API 오류가 발생했습니다. (${resultCode})`)
  }

  return payload
}

function normalizeItems(data) {
  const payload = getPayload(data)
  const item = payload?.body?.items?.item

  if (!item) return []
  return Array.isArray(item) ? item : [item]
}

function removeHtmlTags(value = '') {
  return String(value)
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function extractHomepageUrl(homepage = '') {
  const hrefMatch = String(homepage).match(/href=["']([^"']+)["']/i)

  if (hrefMatch) return hrefMatch[1]
  return removeHtmlTags(homepage)
}

async function requestTourApi(path, params = {}) {
  if (!isProduction && !commonParams.serviceKey) {
    throw new Error('VITE_TOUR_API_KEY가 설정되어 있지 않습니다.')
  }

  const searchParams = new URLSearchParams({
    ...commonParams,
    ...params,
  })

  const response = await fetch(`${TOUR_API_BASE_URL}${path}?${searchParams}`)

  if (!response.ok) {
    const errorText = await response.text().catch(() => '')
    throw new Error(`관광 API 요청 실패 (${response.status})${errorText ? `: ${errorText}` : ''}`)
  }

  return response.json()
}

export async function getSeoulTourList(numOfRows = 10) {
  const data = await requestTourApi('/areaBasedList2', {
    areaCode: '1',
    contentTypeId: '12',
    arrange: 'A',
    numOfRows,
    pageNo: 1,
  })

  return normalizeItems(data).filter((tour) => tour.contentid)
}

export async function getTourDetail(contentId) {
  const data = await requestTourApi('/detailCommon2', { contentId })
  const detail = normalizeItems(data)[0]

  if (!detail) {
    throw new Error(`관광지 상세 정보가 없습니다. contentId: ${contentId}`)
  }

  return {
    contentId: detail.contentid,
    contentTypeId: detail.contenttypeid,
    name: detail.title || '이름 정보 없음',
    imageUrl: detail.firstimage || detail.firstimage2 || '',
    thumbnailUrl: detail.firstimage2 || detail.firstimage || '',
    address: [detail.addr1, detail.addr2].filter(Boolean).join(' '),
    address1: detail.addr1 || '',
    address2: detail.addr2 || '',
    tel: removeHtmlTags(detail.tel),
    telName: removeHtmlTags(detail.telname),
    mapX: detail.mapx || '',
    mapY: detail.mapy || '',
    overview: removeHtmlTags(detail.overview),
    homepage: extractHomepageUrl(detail.homepage),
  }
}

export async function getTourCards(numOfRows = 20) {
  const tourList = await getSeoulTourList(numOfRows)

  return tourList.map((tour) => ({
    contentId: tour.contentid,
    contentTypeId: tour.contenttypeid,
    name: removeHtmlTags(tour.title || '이름 정보 없음'),
    imageUrl: tour.firstimage || tour.firstimage2 || '',
    thumbnailUrl: tour.firstimage2 || tour.firstimage || '',
    address: [tour.addr1, tour.addr2].filter(Boolean).join(' '),
    address1: tour.addr1 || '',
    address2: tour.addr2 || '',
    tel: '',
    telName: '',
    mapX: tour.mapx || '',
    mapY: tour.mapy || '',
    overview: '',
    homepage: '',
  }))
}
