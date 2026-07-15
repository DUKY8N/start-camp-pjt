<script setup>
import BoardList from '@/components/BoardList.vue'
</script>

<template>
  <section class="board-page">
    <div class="board-header">
      <div>
        <p class="eyebrow">Seoul Travel Community</p>
        <h1>게시판</h1>
        <p class="description">서울 관광지 후기, 질문, 코스 추천을 자유롭게 나눠보세요.</p>
      </div>

      <RouterLink class="write-button" to="/board/write">글쓰기</RouterLink>
    </div>

    <BoardList />
  </section>
</template>

<style scoped>
.board-page {
  display: grid;
  gap: 24px;
}

.board-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
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

.description {
  margin: 12px 0 0;
  color: #4b5563;
  font-size: 17px;
}

.write-button {
  flex: 0 0 auto;
  padding: 12px 18px;
  border: 0;
  border-radius: 999px;
  color: white;
  background: #111827;
  font-weight: 800;
  text-decoration: none;
  cursor: pointer;
}


@media (max-width: 760px) {
  .board-header {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
