<script setup>
import { computed, ref } from 'vue'
import FeaturedTourSection from '@/components/FeaturedTourSection.vue'
import SeoulWeatherMap from '@/components/SeoulWeatherMap.vue'
import TourWeatherCard from '@/components/TourWeatherCard.vue'

const selectedTour = ref(null)

function formatDateInput(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const selectedDate = ref(formatDateInput(new Date()))

const minDate = computed(() => formatDateInput(new Date()))
const maxDate = computed(() => {
  const nextWeek = new Date()
  nextWeek.setDate(nextWeek.getDate() + 7)
  return formatDateInput(nextWeek)
})

function changeDate(days) {
  const nextDate = new Date(`${selectedDate.value}T00:00:00`)
  nextDate.setDate(nextDate.getDate() + days)
  selectedDate.value = formatDateInput(nextDate)
}
</script>

<template>
  <section class="area-banner">
    <div class="banner-content">
      <p class="eyebrow">서울 관광지 커뮤니티</p>
      <h1>서울의 매력적인 권역을 함께 발견해요</h1>
      <p class="description">
        한강, 고궁, 도심 골목, 야경 명소까지 서울 곳곳의 관광지를 소개하고
        여행 팁과 후기를 나누는 공간입니다.
      </p>
      <RouterLink class="banner-button" to="/board">게시판 둘러보기</RouterLink>
    </div>
  </section>

  <section class="content-grid">
    <FeaturedTourSection class="content-main" @update:current-tour="selectedTour = $event" />
    <div class="weather-panel">
      <div class="date-picker">
        <button type="button" class="date-button" :disabled="selectedDate === minDate" @click="changeDate(-1)">
          ←
        </button>
        <label class="date-picker-label">
          <span>날짜</span>
          <input v-model="selectedDate" type="date" :min="minDate" :max="maxDate" />
        </label>
        <button type="button" class="date-button" :disabled="selectedDate === maxDate" @click="changeDate(1)">
          →
        </button>
      </div>
      <SeoulWeatherMap :selected-date="selectedDate" />
    </div>
    <TourWeatherCard :tour="selectedTour" :selected-date="selectedDate" />
  </section>
</template>

<style scoped>
.area-banner {
  min-height: 420px;
  display: flex;
  align-items: center;
  padding: 48px;
  border-radius: 24px;
  overflow: hidden;
  color: white;
  background:
    linear-gradient(90deg, rgba(17, 24, 39, 0.78), rgba(17, 24, 39, 0.2)),
    url('https://cdn.sanity.io/images/nxpteyfv/goguides/0eb842b90b1bf6ba40c2af039c62640ce2745597-1600x1066.jpg') center/cover;
}

.banner-content {
  max-width: 560px;
}

.eyebrow {
  margin: 0 0 12px;
  font-size: 15px;
  font-weight: 700;
  color: #86efac;
}

h1 {
  margin: 0;
  font-size: 42px;
  line-height: 1.2;
}

.description {
  margin: 20px 0 28px;
  font-size: 18px;
  line-height: 1.7;
  color: #f3f4f6;
}

.banner-button {
  display: inline-block;
  padding: 12px 20px;
  border-radius: 999px;
  color: #111827;
  background: white;
  font-weight: 700;
  text-decoration: none;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
  margin-top: 24px;
}

.content-main {
  grid-row: 1 / 3;
}

.weather-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.date-picker {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  background: #ffffff;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.date-button {
  flex-shrink: 0;
  border: none;
  border-radius: 999px;
  color: #111827;
  background: #f3f4f6;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
  padding: 4px 8px;
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.date-button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.date-picker-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #4b5563;
  font-size: 13px;
  font-weight: 700;
  min-width: 0;
  flex: 1;
}

.date-picker-label span {
  flex-shrink: 0;
}

.date-picker-label input {
  flex: 1 1 auto;
  min-width: 0;
  width: 110px;
  border: none;
  background: transparent;
  color: #111827;
  font-size: 13px;
  font-weight: 700;
}

.date-picker-label input:focus {
  outline: none;
}

.content-placeholder {
  min-height: 260px;
  border: 1px dashed #d1d5db;
  border-radius: 20px;
  background: #f9fafb;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    gap: 16px;
  }

  .content-main {
    grid-row: auto;
  }
}

@media (max-width: 640px) {
  .area-banner {
    min-height: 360px;
    padding: 32px 24px;
  }

  h1 {
    font-size: 32px;
  }

  .description {
    font-size: 16px;
  }

  .date-picker {
    flex-wrap: nowrap;
    border-radius: 18px;
    padding: 8px 10px;
    max-width: 100%;
  }

  .date-picker-label {
    width: auto;
    justify-content: center;
  }

  .date-picker-label input {
    width: 100px;
    text-align: center;
  }

  .banner-button {
    display: block;
    width: 100%;
    text-align: center;
  }
}
</style>
