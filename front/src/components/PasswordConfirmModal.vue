<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '비밀번호 확인',
  },
  description: {
    type: String,
    default: '작성자 확인을 위해 비밀번호를 입력해주세요.',
  },
  confirmText: {
    type: String,
    default: '확인',
  },
})

const emit = defineEmits(['close', 'confirm'])

const password = ref('')

watch(
  () => props.open,
  (open) => {
    if (open) {
      password.value = ''
    }
  },
)

function closeModal() {
  emit('close')
}

function submitPassword() {
  emit('confirm', password.value)
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="closeModal">
      <section class="modal-card" role="dialog" aria-modal="true" :aria-label="title">
        <button type="button" class="close-button" aria-label="닫기" @click="closeModal">×</button>

        <div class="modal-header">
          <h2>{{ title }}</h2>
          <p>{{ description }}</p>
        </div>

        <form class="modal-form" @submit.prevent="submitPassword">
          <label>
            <span>비밀번호</span>
            <input v-model="password" type="password" placeholder="비밀번호 입력" autofocus />
          </label>

          <div class="modal-actions">
            <button type="button" class="cancel-button" @click="closeModal">취소</button>
            <button type="submit" class="confirm-button" :disabled="!password">
              {{ confirmText }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(4px);
}

.modal-card {
  position: relative;
  width: min(100%, 420px);
  padding: 28px;
  border-radius: 22px;
  background: #ffffff;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.24);
}

.close-button {
  position: absolute;
  top: 14px;
  right: 16px;
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: 50%;
  color: #6b7280;
  background: #f3f4f6;
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
}

.modal-header h2 {
  margin: 0;
  color: #111827;
  font-size: 24px;
}

.modal-header p {
  margin: 10px 0 0;
  color: #6b7280;
  line-height: 1.6;
}

.modal-form {
  display: grid;
  gap: 20px;
  margin-top: 24px;
}

label {
  display: grid;
  gap: 8px;
  color: #374151;
  font-size: 14px;
  font-weight: 800;
}

input {
  width: 100%;
  padding: 13px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  color: #111827;
  outline: none;
}

input:focus {
  border-color: #047857;
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.12);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-actions button {
  min-width: 80px;
  padding: 11px 15px;
  border-radius: 999px;
  font-weight: 800;
  cursor: pointer;
}

.cancel-button {
  color: #374151;
  border: 1px solid #e5e7eb;
  background: white;
}

.confirm-button {
  color: white;
  border: 1px solid #111827;
  background: #111827;
}

.confirm-button:disabled {
  border-color: #d1d5db;
  background: #d1d5db;
  cursor: not-allowed;
}
</style>
