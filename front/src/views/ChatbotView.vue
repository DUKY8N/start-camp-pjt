<script setup>
import { ref } from 'vue'

const messages = ref([
  {
    id: 1,
    role: 'assistant',
    text: '안녕하세요. 서울 관광지, 여행 코스, 날씨에 맞는 장소를 물어보세요.',
  },
  {
    id: 2,
    role: 'user',
    text: '비 오는 날 서울에서 갈 만한 곳 추천해줘',
  },
  {
    id: 3,
    role: 'assistant',
    text: '비 오는 날에는 국립중앙박물관, DDP 전시, 코엑스 별마당도서관 같은 실내 관광지를 추천해요.',
  },
])

const messageInput = ref('')

async function sendMessage() {
  const text = messageInput.value.trim()

  if (!text) return

  const id = Date.now()

  // 사용자 메시지 추가
  messages.value.push({
    id,
    role: 'user',
    text,
  })

  messageInput.value = ''

  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: text,
      }),
    })

    if (!response.ok) {
      throw new Error('API 요청 실패')
    }

    const data = await response.json()

    messages.value.push({
      id: id + 1,
      role: 'assistant',
      text: data.answer,
    })
  } catch (err) {
    messages.value.push({
      id: id + 1,
      role: 'assistant',
      text: '죄송합니다. 현재 답변을 가져오지 못했습니다.',
    })

    console.error(err)
  }
}
</script>

<template>
  <section class="chat-page">
    <header class="chat-header">
      <p class="eyebrow">Seoul Travel Assistant</p>
      <h1>쳇봇</h1>
      <p>서울 여행에 대해 궁금한 내용을 편하게 물어보세요.</p>
    </header>

    <div class="chat-panel">
      <div class="message-list">
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
      </div>

      <form class="chat-input-wrap" @submit.prevent="sendMessage">
        <input v-model="messageInput" type="text" placeholder="메시지를 입력하세요" />
        <button type="submit">전송</button>
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
  word-break: keep-all;
}

.message-row.user .message-bubble {
  color: white;
  background: #111827;
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
}

.chat-input-wrap input:focus {
  border-color: #047857;
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.12);
}

.chat-input-wrap button {
  min-width: 78px;
  padding: 0 18px;
  border: 0;
  border-radius: 999px;
  color: white;
  background: #111827;
  font-weight: 800;
  cursor: pointer;
}

@media (max-width: 640px) {
  .chat-header {
    padding: 24px;
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
}
</style>
