// 백엔드 API 서버의 기본 주소
// Vite 환경변수가 있으면 그 값을 사용하고, 없으면 Render 백엔드 주소로 연결
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'https://start-camp-pjt-1.onrender.com').replace(/\/$/, '')

// 요청 URL을 만들기 위한 헬퍼 함수
// path: API 경로, params: 쿼리 파라미터
function buildUrl(path, params = {}) {
  const url = new URL(path, API_BASE_URL)

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }

    url.searchParams.append(key, String(value))
  })

  return url.toString()
}

// 모든 API 요청에서 공통으로 사용하는 함수
// fetch 기반으로 요청을 보내고, 응답을 파싱한 뒤 에러를 표준화해서 반환
async function request(path, { method = 'GET', params, body, headers = {}, ...options } = {}) {
  const isJsonBody = body !== undefined && !(body instanceof FormData)
  const url = buildUrl(path, params)

  try {
    console.info('[API] 요청 시작', { method, url, body })

    const response = await fetch(url, {
      method,
      headers: {
        ...(isJsonBody ? { 'Content-Type': 'application/json' } : {}),
        ...headers,
      },
      body: body == null ? undefined : isJsonBody ? JSON.stringify(body) : body,
      ...options,
    })

    console.info('[API] 응답 수신', { method, url, status: response.status })

    const contentType = response.headers.get('content-type') || ''
    const isJsonResponse = contentType.includes('application/json')
    const payload = isJsonResponse ? await response.json() : await response.text()

    if (!response.ok) {
      const error = new Error(payload?.message || `요청 실패: ${response.status}`)
      error.status = response.status
      error.payload = payload
      throw error
    }

    return payload
  } catch (error) {
    console.error('[API] 요청 실패', { method, url, error })

    if (error instanceof Error && error.name === 'TypeError') {
      const networkError = new Error(`네트워크 요청 실패: ${url}`)
      networkError.cause = error
      throw networkError
    }

    throw error
  }
}

// TanStack Query에서 사용할 게시글 캐시 키
// 목록 조회와 상세 조회를 분리해서 캐싱할 수 있도록 구성
export const postQueryKeys = {
  all: ['posts'],
  list: (keyword = '') => [...postQueryKeys.all, 'list', keyword],
  detail: (postId) => [...postQueryKeys.all, 'detail', postId],
}

// 게시글 목록 조회용 Query 옵션을 생성
// Vue Query의 useQuery()에서 바로 사용할 수 있는 형태로 반환
export function getPostsQueryOptions(keyword = '') {
  return {
    queryKey: postQueryKeys.list(keyword),
    queryFn: () => getPosts(keyword),
  }
}

// 게시글 상세 조회용 Query 옵션을 생성
// postId가 없으면 실행되지 않도록 enabled 조건을 추가
export function getPostQueryOptions(postId) {
  return {
    queryKey: postQueryKeys.detail(postId),
    queryFn: () => getPost(postId),
    enabled: Boolean(postId),
  }
}

// 게시글 목록 조회 API
// keyword가 있으면 검색어를 쿼리 파라미터로 전달
export function getPosts(keyword = '') {
  return request('/posts', {
    params: keyword ? { keyword } : {},
  })
}

// 특정 게시글 1개 조회 API
export function getPost(postId) {
  return request(`/posts/${postId}`)
}

// 새 게시글 작성 API
// 입력값을 정규화한 뒤 서버에 전송
export function createPost(payload) {
  const normalizedPayload = {
    category: String(payload?.category ?? '').trim(),
    title: String(payload?.title ?? '').trim(),
    content: String(payload?.content ?? '').trim(),
    password: String(payload?.password ?? '').trim(),
  }

  return request('/posts', {
    method: 'POST',
    body: normalizedPayload,
  })
}

// 기존 게시글 수정 API
export function updatePost(postId, payload) {
  return request(`/posts/${postId}`, {
    method: 'PUT',
    body: payload,
  })
}

// 게시글 삭제 API
// 비밀번호를 body에 담아 서버로 전달
export function deletePost(postId, password) {
  const trimmedPassword = String(password ?? '').trim()

  return request(`/posts/${postId}`, {
    method: 'DELETE',
    body: {
      password: trimmedPassword,
    },
  })
}

// 챗봇 질문 전송 API
export function chatWithBot(question) {
  return request('/api/chat', {
    method: 'POST',
    body: { question },
  })
}
