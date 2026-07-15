<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { getPostsQueryOptions } from '@/api/backend'

const PAGE_SIZE = 15
const currentPage = ref(1)

function formatDate(value) {
  if (!value) return ''

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

function normalizePost(post) {
  return {
    id: post.id,
    title: post.title,
    author: post.category || '익명',
    createdAt: formatDate(post.created_at),
    content: post.content,
    views: post.views ?? 0,
  }
}

const { data, isLoading, isError, error } = useQuery(getPostsQueryOptions())

const posts = computed(() => {
  const rawPosts = Array.isArray(data.value) ? data.value : []
  return rawPosts.map(normalizePost)
})

const totalPages = computed(() => Math.max(1, Math.ceil(posts.value.length / PAGE_SIZE)))
const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))
const pagedPosts = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return posts.value.slice(start, start + PAGE_SIZE)
})

function goPreviousPage() {
  if (currentPage.value > 1) {
    currentPage.value -= 1
  }
}

function goNextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1
  }
}
</script>

<template>
  <div class="board-list-wrap">
    <div v-if="isLoading" class="state-card">게시글을 불러오는 중입니다...</div>
    <div v-else-if="isError" class="state-card error">
      게시글을 불러오지 못했습니다.
      <span>{{ error?.message }}</span>
    </div>

    <template v-else>
      <div class="board-list">
        <div class="list-header">
          <span>제목</span>
          <span>카테고리</span>
          <span>생성날짜</span>
        </div>

        <RouterLink v-for="post in pagedPosts" :key="post.id" class="post-row" :to="`/board/${post.id}`">
          <div class="post-main">
            <h2>{{ post.title }}</h2>
            <p class="preview">{{ post.content }}</p>
          </div>
          <span class="author">{{ post.author }}</span>
          <time :datetime="post.createdAt">{{ post.createdAt }}</time>
        </RouterLink>
      </div>

      <nav v-if="posts.length" class="pagination" aria-label="게시판 페이지">
        <button
          type="button"
          class="page-arrow"
          :disabled="currentPage === 1"
          aria-label="이전 페이지"
          @click="goPreviousPage"
        >
          &lt;
        </button>

        <button
          v-for="page in pageNumbers"
          :key="page"
          type="button"
          :class="{ active: page === currentPage }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>

        <button
          type="button"
          class="page-arrow"
          :disabled="currentPage === totalPages"
          aria-label="다음 페이지"
          @click="goNextPage"
        >
          &gt;
        </button>
      </nav>
    </template>
  </div>
</template>

<style scoped>
.board-list-wrap {
  display: grid;
  gap: 20px;
}

.state-card {
  padding: 28px;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
  color: #4b5563;
}

.state-card.error {
  color: #b91c1c;
}

.board-list {
  overflow: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
}

.list-header,
.post-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px 120px;
  align-items: center;
  gap: 16px;
}

.list-header {
  padding: 14px 22px;
  color: #6b7280;
  background: #f9fafb;
  font-size: 14px;
  font-weight: 800;
}

.post-row {
  padding: 18px 22px;
  border-top: 1px solid #f3f4f6;
  text-decoration: none;
  transition: background 0.2s ease;
  cursor: pointer;
}

.post-row:hover {
  background: #f9fafb;
}

.post-main {
  display: grid;
  gap: 6px;
}

h2 {
  overflow: hidden;
  margin: 0;
  color: #111827;
  font-size: 17px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.author,
time {
  color: #6b7280;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.pagination button {
  min-width: 38px;
  height: 38px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  color: #4b5563;
  background: #ffffff;
  font-weight: 800;
  cursor: pointer;
}

.pagination button.active {
  color: #ffffff;
  border-color: #111827;
  background: #111827;
}

.pagination button:disabled {
  color: #d1d5db;
  background: #f9fafb;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .list-header {
    display: none;
  }

  .post-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  h2,
  .preview {
    white-space: normal;
  }
}
</style>
