<script setup>
import { reactive, ref } from 'vue'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useRouter } from 'vue-router'
import { createPost, postQueryKeys } from '@/api/backend'

const router = useRouter()
const queryClient = useQueryClient()

const form = reactive({
  title: '',
  author: '',
  password: '',
  body: '',
})
const isSubmitting = ref(false)

const createMutation = useMutation({
  mutationFn: (payload) => createPost(payload),
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: postQueryKeys.all })
    router.push('/board')
  },
  onError: (err) => {
    isSubmitting.value = false
    alert(err?.message || '게시글 등록에 실패했습니다.')
  },
  onSettled: () => {
    isSubmitting.value = false
  },
})

function cancelWrite() {
  router.push('/board')
}

function submitPost() {
  if (!form.title.trim() || !form.body.trim() || !form.password.trim()) {
    alert('제목, 내용, 비밀번호를 모두 입력해주세요.')
    return
  }

  isSubmitting.value = true
  createMutation.mutate({
    category: 'general',
    title: form.title.trim(),
    content: form.body.trim(),
    password: form.password.trim(),
  })
}
</script>

<template>
  <section class="write-page">
    <div class="write-header">
      <p class="eyebrow">New Post</p>
      <h1>게시글 작성</h1>
      <p>서울 여행 이야기를 자유롭게 남겨주세요.</p>
    </div>

    <form class="write-form" @submit.prevent="submitPost">
      <label>
        <span>제목</span>
        <input v-model="form.title" type="text" placeholder="제목을 입력하세요" required />
      </label>

      <div class="form-grid">
        <label>
          <span>작성자</span>
          <input v-model="form.author" type="text" placeholder="작성자명" />
        </label>

        <label>
          <span>비밀번호</span>
          <input v-model="form.password" type="password" placeholder="수정/삭제용 비밀번호" required />
        </label>
      </div>

      <label>
        <span>내용</span>
        <textarea v-model="form.body" placeholder="내용을 입력하세요" required></textarea>
      </label>

      <div class="form-actions">
        <button type="button" class="cancel-button" @click="cancelWrite">취소</button>
        <button type="submit" class="submit-button" :disabled="isSubmitting">
          {{ isSubmitting ? '등록 중...' : '등록' }}
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.write-page {
  display: grid;
  gap: 24px;
}

.write-header {
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
  font-size: 36px;
}

.write-header p:last-child {
  margin: 12px 0 0;
  color: #4b5563;
  font-size: 17px;
}

.write-form {
  display: grid;
  gap: 22px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  background: #ffffff;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
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
  min-height: 280px;
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
  padding-top: 4px;
}

.form-actions button {
  min-width: 92px;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 800;
  cursor: pointer;
}

.cancel-button {
  color: #374151;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

.submit-button {
  color: #ffffff;
  border: 1px solid #111827;
  background: #111827;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: wait;
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .write-header,
  .write-form {
    padding: 24px;
  }

  h1 {
    font-size: 30px;
  }
}
</style>
