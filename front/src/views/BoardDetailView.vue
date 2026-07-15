<script setup>
import { computed, ref } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useRoute, useRouter } from 'vue-router'
import PasswordConfirmModal from '@/components/PasswordConfirmModal.vue'
import { deletePost, getPostQueryOptions, postQueryKeys } from '@/api/backend'

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()

const postId = computed(() => Number(route.params.id))

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

const { data: postResponse, isLoading, isError, error } = useQuery(
  computed(() => getPostQueryOptions(postId.value)),
)

const deleteMutation = useMutation({
  mutationFn: (password) => deletePost(postId.value, password),
  onSuccess: async () => {
    isDeleting.value = false

    try {
      await queryClient.invalidateQueries({ queryKey: postQueryKeys.all })
    } catch (invalidateError) {
      console.warn('[BoardDetail] 게시글 목록 캐시 갱신 실패', invalidateError)
    }

    router.replace('/board')
  },
  onError: (err) => {
    isDeleting.value = false
    alert(err?.message || '삭제에 실패했습니다.')
  },
  onSettled: () => {
    isDeleting.value = false
  },
})

const post = computed(() => {
  if (!postResponse.value) return null

  return {
    id: postResponse.value.id,
    title: postResponse.value.title,
    author: postResponse.value.category || '익명',
    createdAt: formatDate(postResponse.value.created_at),
    body: postResponse.value.content,
    views: postResponse.value.views ?? 0,
  }
})

const modalOpen = ref(false)
const modalMode = ref('')
const isDeleting = ref(false)

const modalTitle = computed(() => (modalMode.value === 'delete' ? '게시글 삭제' : '게시글 수정'))
const modalDescription = computed(() =>
  modalMode.value === 'delete'
    ? '게시글을 삭제하려면 작성 시 설정한 비밀번호를 입력해주세요.'
    : '게시글을 수정하려면 작성 시 설정한 비밀번호를 입력해주세요.',
)
const modalConfirmText = computed(() => (modalMode.value === 'delete' ? '삭제' : '수정'))

function goBack() {
  router.push('/board')
}

function openPasswordModal(mode) {
  modalMode.value = mode
  modalOpen.value = true
}

function closePasswordModal() {
  modalOpen.value = false
  modalMode.value = ''
}

function handlePasswordConfirm(password) {
  if (modalMode.value === 'delete') {
    isDeleting.value = true
    closePasswordModal()
    router.replace('/board')

    deleteMutation.mutate(password)
    return
  }

  if (modalMode.value === 'edit') {
    closePasswordModal()
    router.push({
      path: `/board/${postId.value}/edit`,
      query: { password },
    })
  }
}
</script>

<template>
  <section class="detail-page">
    <button type="button" class="back-button" @click="goBack">← 뒤로가기</button>

    <article v-if="isLoading" class="empty-card">
      <h1>게시글을 불러오는 중입니다.</h1>
    </article>

    <article v-else-if="isError" class="empty-card">
      <h1>게시글 정보를 불러오지 못했습니다.</h1>
      <p>{{ error?.message }}</p>
    </article>

    <article v-else-if="post" class="detail-card">
      <header class="detail-header">
        <h1>{{ post.title }}</h1>

        <div class="post-meta">
          <span>카테고리 {{ post.author }}</span>
          <time :datetime="post.createdAt">{{ post.createdAt }}</time>
          <span>조회수 {{ post.views }}</span>
        </div>
      </header>

      <div class="post-body">
        {{ post.body }}
      </div>

      <footer class="detail-actions">
        <button type="button" class="delete-button" :disabled="isDeleting" @click="openPasswordModal('delete')">
          {{ isDeleting ? '삭제 중...' : '삭제' }}
        </button>
        <button type="button" class="edit-button" @click="openPasswordModal('edit')">수정</button>
      </footer>
    </article>

    <article v-else class="empty-card">
      <h1>게시글을 찾을 수 없습니다.</h1>
      <p>삭제되었거나 존재하지 않는 게시글입니다.</p>
    </article>

    <PasswordConfirmModal
      :open="modalOpen"
      :title="modalTitle"
      :description="modalDescription"
      :confirm-text="modalConfirmText"
      @close="closePasswordModal"
      @confirm="handlePasswordConfirm"
    />
  </section>
</template>

<style scoped>
.detail-page {
  display: grid;
  gap: 18px;
}

.back-button {
  justify-self: start;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  color: #374151;
  background: #ffffff;
  font-weight: 800;
  cursor: pointer;
}

.detail-card,
.empty-card {
  overflow: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  background: #ffffff;
}

.detail-header {
  padding: 34px 36px 28px;
  border-bottom: 1px solid #f3f4f6;
  background: linear-gradient(135deg, #f9fafb, #ecfdf5);
}

h1 {
  margin: 0;
  color: #111827;
  font-size: 34px;
  line-height: 1.35;
  word-break: keep-all;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin-top: 16px;
  color: #6b7280;
  font-size: 15px;
  font-weight: 700;
}

.post-body {
  min-height: 280px;
  padding: 36px;
  color: #374151;
  font-size: 18px;
  line-height: 1.85;
  white-space: pre-line;
  word-break: keep-all;
}

.detail-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px 36px 28px;
  border-top: 1px solid #f3f4f6;
}

.detail-actions button {
  min-width: 86px;
  padding: 11px 16px;
  border-radius: 999px;
  font-weight: 800;
  cursor: pointer;
}

.delete-button {
  color: #b91c1c;
  border: 1px solid #fecaca;
  background: #fff1f2;
}

.edit-button {
  color: #ffffff;
  border: 1px solid #111827;
  background: #111827;
}

.empty-card {
  padding: 42px;
  text-align: center;
}

.empty-card p {
  color: #6b7280;
}

@media (max-width: 640px) {
  .detail-header,
  .post-body,
  .detail-actions {
    padding-left: 22px;
    padding-right: 22px;
  }

  h1 {
    font-size: 26px;
  }

  .post-body {
    font-size: 16px;
  }
}
</style>
