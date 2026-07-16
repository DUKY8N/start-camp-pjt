<script setup>
import { nextTick, ref } from 'vue'
import { chatWithBot } from '@/api/backend'

const messages = ref([
  {
    id: 1,
    role: 'assistant',
    text: '안녕하세요. 서울 관광지, 여행 코스, 날씨에 맞는 장소를 물어보세요.',
  },
])

const messageInput = ref('')
const isLoading = ref(false)
const messageListRef = ref(null)

let messageId = 2

async function scrollToBottom() {
  await nextTick()

  if (!messageListRef.value) return

  messageListRef.value.scrollTop =
    messageListRef.value.scrollHeight
}

async function sendMessage() {
  const text = messageInput.value.trim()

  if (!text || isLoading.value) return

  messages.value.push({
    id: messageId++,
    role: 'user',
    text,
  })

  messageInput.value = ''
  isLoading.value = true

  await scrollToBottom()

  try {
    const data = await chatWithBot(text)

    messages.value.push({
      id: messageId++,
      role: 'assistant',
      text: data.answer || '답변 내용이 없습니다.',
    })
  } catch (error) {
    console.error('챗봇 API 오류:', error)

    messages.value.push({
      id: messageId++,
      role: 'assistant',
      text:
        error instanceof Error
          ? `죄송합니다. ${error.message}`
          : '죄송합니다. 현재 답변을 가져오지 못했습니다.',
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}
</script>

<template>
  <section class="chat-page">
    <header class="chat-header">
      <p class="eyebrow">Seoul Travel Assistant</p>
      <h1>챗봇</h1>
      <p>서울 여행에 대해 궁금한 내용을 편하게 물어보세요.</p>
    </header>

    <div class="chat-panel">
      <div
        ref="messageListRef"
        class="message-list"
      >
        <article
          v-for="message in messages"
          :key="message.id"
          class="message-row"
          :class="message.role"
        >
          <div class="avatar">
            {{ message.role === 'assistant' ? 'AI' : '나' }}
          </div>

          <div class="message-bubble">
            {{ message.text }}
          </div>
        </article>

        <article
          v-if="isLoading"
          class="message-row assistant"
        >
          <div class="avatar">
            AI
          </div>

          <div class="message-bubble loading-bubble">
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
          </div>
        </article>
      </div>

      <form
        class="chat-input-wrap"
        @submit.prevent="sendMessage"
      >
        <input
          v-model="messageInput"
          type="text"
          placeholder="메시지를 입력하세요"
          autocomplete="off"
          :disabled="isLoading"
        />

        <button
          type="submit"
          :disabled="isLoading || !messageInput.trim()"
        >
          {{ isLoading ? '답변 중' : '전송' }}
        </button>
      </form>
    </div>
  </section>
</template>
<style scoped>
.chat-page {
  display: grid;
  gap: 24px;
}

.chat-header {
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

.chat-header p:last-child {
  margin: 12px 0 0;
  color: #4b5563;
  font-size: 17px;
}

.chat-panel {
  display: grid;
  grid-template-rows: minmax(420px, 1fr) auto;
  overflow: hidden;
  min-height: 620px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  background: #ffffff;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 28px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.message-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.message-row.user {
  flex-direction: row-reverse;
}

.avatar {
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #047857;
  background: #ecfdf5;
  font-size: 13px;
  font-weight: 900;
}

.message-row.user .avatar {
  color: #111827;
  background: #f3f4f6;
}

.message-bubble {
  max-width: min(680px, 78%);
  padding: 14px 16px;
  border-radius: 18px;
  color: #111827;
  background: #f9fafb;
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  word-break: keep-all;
}

.message-row.user .message-bubble {
  color: #ffffff;
  background: #111827;
}

.loading-bubble {
  display: flex;
  align-items: center;
  gap: 5px;
  min-height: 24px;
}

.loading-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #6b7280;
  animation: loading 1.2s infinite ease-in-out;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.15s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes loading {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }

  30% {
    transform: translateY(-5px);
    opacity: 1;
  }
}

.chat-input-wrap {
  display: flex;
  gap: 10px;
  padding: 18px;
  border-top: 1px solid #f3f4f6;
  background: #ffffff;
}

.chat-input-wrap input {
  flex: 1;
  height: 50px;
  padding: 0 16px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  outline: none;
  font-size: 15px;
}

.chat-input-wrap input:focus {
  border-color: #047857;
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.12);
}

.chat-input-wrap input:disabled {
  color: #9ca3af;
  background: #f9fafb;
  cursor: not-allowed;
}

.chat-input-wrap button {
  min-width: 78px;
  padding: 0 18px;
  border: 0;
  border-radius: 999px;
  color: #ffffff;
  background: #111827;
  font-weight: 800;
  cursor: pointer;
}

.chat-input-wrap button:hover:not(:disabled) {
  background: #374151;
}

.chat-input-wrap button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .chat-header {
    padding: 24px;
  }

  h1 {
    font-size: 30px;
  }

  .chat-panel {
    min-height: 560px;
  }

  .message-list {
    padding: 20px;
  }

  .message-bubble {
    max-width: 82%;
  }

  .chat-input-wrap {
    padding: 14px;
  }
}
</style>
