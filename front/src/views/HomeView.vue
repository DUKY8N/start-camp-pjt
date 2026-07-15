<script setup>
import { ref } from 'vue'
import FeaturedTourSection from '@/components/FeaturedTourSection.vue'
import SeoulWeatherMap from '@/components/SeoulWeatherMap.vue'
import TourWeatherCard from '@/components/TourWeatherCard.vue'

const selectedTour = ref(null)
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
    <SeoulWeatherMap />
    <TourWeatherCard :tour="selectedTour" />
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

.content-placeholder {
  min-height: 260px;
  border: 1px dashed #d1d5db;
  border-radius: 20px;
  background: #f9fafb;
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
}
</style>
