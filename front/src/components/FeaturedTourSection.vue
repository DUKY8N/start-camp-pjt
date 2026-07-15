<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { getTourCards } from '@/api/tourApi'
import TourCard from './TourCard.vue'

const emit = defineEmits(['update:current-tour'])

const tours = ref([])
const currentIndex = ref(0)
const loading = ref(false)
const errorMessage = ref('')

const currentTour = computed(() => tours.value[currentIndex.value] ?? null)

watch(currentTour, (tour) => {
  emit('update:current-tour', tour)
})

function showPreviousTour() {
  if (tours.value.length <= 1) return
  currentIndex.value = currentIndex.value === 0 ? tours.value.length - 1 : currentIndex.value - 1
}

function showNextTour() {
  if (tours.value.length <= 1) return
  currentIndex.value = currentIndex.value === tours.value.length - 1 ? 0 : currentIndex.value + 1
}

async function loadTours() {
  loading.value = true
  errorMessage.value = ''

  try {
    tours.value = await getTourCards()
    currentIndex.value = 0
  } catch (error) {
    console.error(error)
    tours.value = []
    errorMessage.value = '서울 관광지 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(loadTours)
</script>

<template>
  <section class="featured-tour">
    <div class="section-header">
      <div>
        <p class="section-subtitle">서울 추천 관광지</p>
        <h2>오늘의 관광지 카드</h2>
      </div>

      <span v-if="tours.length > 0" class="card-count">
        {{ currentIndex + 1 }} / {{ tours.length }}
      </span>
    </div>

    <div class="carousel-container">
      <p v-if="loading" class="state-message">서울 관광지 정보를 불러오는 중입니다.</p>
      <p v-else-if="errorMessage" class="state-message error">{{ errorMessage }}</p>
      <p v-else-if="!currentTour" class="state-message">표시할 관광지가 없습니다.</p>

      <template v-else>
        <button
          type="button"
          class="carousel-button previous-button"
          :disabled="tours.length <= 1"
          aria-label="이전 관광지"
          @click="showPreviousTour"
        >
          ‹
        </button>

        <div class="card-area">
          <Transition name="card-change" mode="out-in">
            <TourCard :key="currentTour.contentId" :tour="currentTour" />
          </Transition>
        </div>

        <button
          type="button"
          class="carousel-button next-button"
          :disabled="tours.length <= 1"
          aria-label="다음 관광지"
          @click="showNextTour"
        >
          ›
        </button>
      </template>
    </div>

    <div v-if="tours.length > 1" class="carousel-indicator">
      <button
        v-for="(tour, index) in tours"
        :key="tour.contentId"
        type="button"
        class="indicator-dot"
        :class="{ active: index === currentIndex }"
        :aria-label="`${index + 1}번째 관광지 보기`"
        @click="currentIndex = index"
      />
    </div>
  </section>
</template>

<style scoped>
.featured-tour {
  min-width: 0;
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.section-subtitle {
  margin: 0 0 7px;
  color: #047857;
  font-size: 14px;
  font-weight: 800;
}

h2 {
  margin: 0;
  color: #111827;
  font-size: 28px;
}

.card-count {
  color: #6b7280;
  font-size: 14px;
  font-weight: 700;
}

.carousel-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 560px;
  padding: 32px 72px;
  background: linear-gradient(145deg, #f7faff 0%, #edfdf5 100%);
  border: 1px solid #dde8f5;
  border-radius: 20px;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 90%), 0 12px 30px rgb(51 78 110 / 7%);
}

.card-area {
  width: min(100%, 570px);
}

.carousel-button {
  position: absolute;
  top: 50%;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  padding: 0;
  color: #047857;
  background: rgb(255 255 255 / 95%);
  border: 1px solid #d5e1f0;
  border-radius: 50%;
  box-shadow: 0 6px 18px rgb(42 68 100 / 14%);
  cursor: pointer;
  font-size: 36px;
  line-height: 1;
  transform: translateY(-50%);
  transition: color 0.2s ease, background-color 0.2s ease, transform 0.2s ease;
}

.carousel-button:hover:not(:disabled) {
  color: #ffffff;
  background: #047857;
  transform: translateY(-50%) scale(1.07);
}

.carousel-button:disabled {
  cursor: default;
  opacity: 0.45;
}

.previous-button {
  left: 14px;
}

.next-button {
  right: 14px;
}

.carousel-indicator {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.indicator-dot {
  width: 9px;
  height: 9px;
  padding: 0;
  background: #d1d5db;
  border: 0;
  border-radius: 999px;
  cursor: pointer;
  transition: width 0.2s, background-color 0.2s;
}

.indicator-dot.active {
  width: 26px;
  background: #047857;
}

.state-message {
  width: 100%;
  margin: 0;
  padding: 70px 20px;
  color: #6b7280;
  text-align: center;
  font-weight: 700;
}

.state-message.error {
  color: #b91c1c;
}

.card-change-enter-active,
.card-change-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.card-change-enter-from {
  opacity: 0;
  transform: translateX(18px);
}

.card-change-leave-to {
  opacity: 0;
  transform: translateX(-18px);
}

@media (max-width: 760px) {
  .carousel-container {
    min-height: 480px;
    padding: 24px 48px;
  }

  .carousel-button {
    width: 38px;
    height: 38px;
    font-size: 30px;
  }

  .previous-button {
    left: 6px;
  }

  .next-button {
    right: 6px;
  }
}
</style>
