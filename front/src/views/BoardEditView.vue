<script setup>
import { reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { boardPosts } from '@/data/boardPosts'

const route = useRoute()
const router = useRouter()

const form = reactive({
  title: '',
  body: '',
})

const postId = Number(route.params.id)
const post = boardPosts.find((item) => item.id === postId)

watch(
  () => post,
  (currentPost) => {
    if (!currentPost) return

    form.title = currentPost.title
    form.body = currentPost.body
  },
  { immediate: true },
)

function cancelEdit() {
  router.push(`/board/${postId}`)
}

function submitEdit() {
  // TODO: API 연결 후 게시글 수정 요청
  // 현재는 더미데이터라 실제 저장 없이 상세 페이지로 이동합니다.
  console.log('게시글 수정:', {
    id: postId,
    title: form.title,
    body: form.body,
  })

  router.push(`/board/${postId}`)
}
</script>

<template>
  <section class="edit-page">
    <div class="edit-header">
      <p class="eyebrow">Edit Post</p>
      <h1>게시글 수정</h1>
      <p>기존 내용을 확인하고 필요한 부분만 수정해주세요.</p>
    </div>

    <form v-if="post" class="edit-form" @submit.prevent="submitEdit">
      <label>
        <span>제목</span>
        <input v-model="form.title" type="text" placeholder="제목을 입력하세요" required />
      </label>

      <label>
        <span>본문</span>
        <textarea v-model="form.body" placeholder="본문을 입력하세요" required></textarea>
      </label>

      <div class="form-actions">
        <button type="button" class="cancel-button" @click="cancelEdit">수정 취소</button>
        <button type="submit" class="submit-button">수정</button>
      </div>
    </form>

    <article v-else class="empty-card">
      <h1>게시글을 찾을 수 없습니다.</h1>
      <p>삭제되었거나 존재하지 않는 게시글입니다.</p>
      <button type="button" @click="router.push('/board')">목록으로</button>
    </article>
  </section>
</template>

<style scoped>
.edit-page {
  display: grid;
  gap: 24px;
}

.edit-header {
  padding: 32px;
  border-radius: 24px;
  background: linear-gradient(135deg, #ecfdf5, #eff6ff);
}

.eyebrow {
  margin: 0 0 8px;
  color: #047857;
  font-size: 14px;
  font-weight: 800;
}

h1 {
  margin: 0;
  color: #111827;
  font-size: 36px;
}

.edit-header p:last-child {
  margin: 12px 0 0;
  color: #4b5563;
  font-size: 17px;
}

.edit-form,
.empty-card {
  display: grid;
  gap: 22px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  background: #ffffff;
}

label {
  display: grid;
  gap: 9px;
  color: #374151;
  font-size: 14px;
  font-weight: 800;
}

input,
textarea {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  color: #111827;
  background: #ffffff;
  outline: none;
}

input {
  height: 48px;
  padding: 0 14px;
}

textarea {
  min-height: 340px;
  padding: 14px;
  resize: vertical;
  line-height: 1.7;
}

input:focus,
textarea:focus {
  border-color: #047857;
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.12);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-actions button,
.empty-card button {
  min-width: 96px;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 800;
  cursor: pointer;
}

.cancel-button,
.empty-card button {
  color: #374151;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

.submit-button {
  color: #ffffff;
  border: 1px solid #111827;
  background: #111827;
}

.empty-card {
  text-align: center;
}

.empty-card p {
  margin: 0;
  color: #6b7280;
}

@media (max-width: 700px) {
  .edit-header,
  .edit-form,
  .empty-card {
    padding: 24px;
  }

  h1 {
    font-size: 30px;
  }
}
</style>
