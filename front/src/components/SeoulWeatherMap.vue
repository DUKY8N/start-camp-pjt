<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Cloud,
  CloudDrizzle,
  CloudFog,
  CloudLightning,
  CloudRain,
  CloudSnow,
  CloudSun,
  Cloudy,
  Sun,
} from '@lucide/vue'

const today = new Intl.DateTimeFormat('ko-KR', {
  month: 'long',
  day: 'numeric',
  weekday: 'long',
}).format(new Date())

const areas = [
  { name: '마포', latitude: 37.5663, longitude: 126.9019, top: '42%', left: '28%' },
  { name: '종로', latitude: 37.5735, longitude: 126.9788, top: '34%', left: '48%' },
  { name: '강남', latitude: 37.5172, longitude: 127.0473, top: '68%', left: '58%' },
  { name: '송파', latitude: 37.5145, longitude: 127.1059, top: '64%', left: '76%' },
  { name: '영등포', latitude: 37.5264, longitude: 126.8962, top: '58%', left: '28%' },
]

const weatherItems = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const badgeText = computed(() => {
  if (isLoading.value) return 'LOADING'
  if (errorMessage.value) return 'ERROR'
  return 'LIVE'
})

function getWeatherText(code) {
  if (code === 0) return '맑음'
  if ([1, 2].includes(code)) return '대체로 맑음'
  if (code === 3) return '흐림'
  if ([45, 48].includes(code)) return '안개'
  if (code >= 51 && code <= 57) return '이슬비'
  if (code >= 61 && code <= 67) return '비'
  if (code >= 71 && code <= 77) return '눈'
  if (code >= 80 && code <= 82) return '소나기'
  if (code >= 95 && code <= 99) return '뇌우'
  return '알 수 없음'
}

function getWeatherIcon(code) {
  if (code === 0) return Sun
  if ([1, 2].includes(code)) return CloudSun
  if (code === 3) return Cloudy
  if ([45, 48].includes(code)) return CloudFog
  if (code >= 51 && code <= 57) return CloudDrizzle
  if (code >= 61 && code <= 67) return CloudRain
  if (code >= 71 && code <= 77) return CloudSnow
  if (code >= 80 && code <= 82) return CloudRain
  if (code >= 95 && code <= 99) return CloudLightning
  return Cloud
}

async function fetchWeather(area) {
  const params = new URLSearchParams({
    latitude: area.latitude,
    longitude: area.longitude,
    current: 'temperature_2m,weather_code',
    timezone: 'Asia/Seoul',
  })

  const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`)

  if (!response.ok) {
    throw new Error(`${area.name} 날씨를 불러오지 못했습니다.`)
  }

  const data = await response.json()

  return {
    ...area,
    temp: Math.round(data.current.temperature_2m),
    weather: getWeatherText(data.current.weather_code),
    icon: getWeatherIcon(data.current.weather_code),
  }
}

onMounted(async () => {
  try {
    weatherItems.value = await Promise.all(areas.map(fetchWeather))
  } catch (error) {
    errorMessage.value = error.message || '날씨 정보를 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section class="weather-card">
    <div class="weather-header">
      <div>
        <p class="date">{{ today }}</p>
        <h2>서울 권역 날씨</h2>
      </div>
      <span class="badge" :class="{ 'is-error': errorMessage }">{{ badgeText }}</span>
    </div>

    <div class="map-wrap">
      <img src="@/assets/images/seoul-districts.svg" alt="서울 행정구역 지도" />

      <p v-if="isLoading" class="status-message">날씨 정보를 불러오는 중...</p>
      <p v-else-if="errorMessage" class="status-message is-error">{{ errorMessage }}</p>

      <div
        v-for="point in weatherItems"
        v-else
        :key="point.name"
        class="weather-point"
        :style="{ top: point.top, left: point.left }"
      >
        <strong>{{ point.name }}</strong>
        <component :is="point.icon" class="point-icon" :size="16" :stroke-width="2.4" />
        <span>{{ point.temp }}°</span>
        <small>{{ point.weather }}</small>
      </div>
    </div>

    <p class="source">Weather: Open-Meteo · Map: Wikimedia Commons, CC BY-SA 3.0</p>
  </section>
</template>

<style scoped>
.weather-card {
  height: 100%;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: #ffffff;
}

.weather-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.date {
  margin: 0 0 4px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 600;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.badge {
  padding: 5px 8px;
  border-radius: 999px;
  color: #047857;
  background: #d1fae5;
  font-size: 12px;
  font-weight: 800;
}

.badge.is-error {
  color: #b91c1c;
  background: #fee2e2;
}

.map-wrap {
  position: relative;
  min-height: 170px;
  border-radius: 16px;
  background: #f0f9ff;
  overflow: hidden;
}

.map-wrap img {
  width: 100%;
  height: 100%;
  min-height: 170px;
  object-fit: contain;
  padding: 10px;
  opacity: 0.78;
}

.status-message {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  margin: 0;
  padding: 20px;
  color: #6b7280;
  background: rgba(240, 249, 255, 0.72);
  text-align: center;
  font-size: 14px;
  font-weight: 700;
}

.status-message.is-error {
  color: #b91c1c;
}

.weather-point {
  position: absolute;
  transform: translate(-50%, -50%);
  display: grid;
  gap: 1px;
  min-width: 54px;
  padding: 6px 8px;
  border-radius: 12px;
  color: #111827;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.14);
  text-align: center;
  font-size: 12px;
}

.point-icon {
  justify-self: center;
  color: #047857;
}

.weather-point span {
  font-size: 17px;
  font-weight: 800;
}

.weather-point small {
  color: #6b7280;
  font-size: 11px;
}

.source {
  margin: 10px 0 0;
  color: #9ca3af;
  font-size: 11px;
}
</style>
