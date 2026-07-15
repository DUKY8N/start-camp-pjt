<script setup>
import { computed, ref, watch } from 'vue'
import {
  Cloud,
  CloudDrizzle,
  CloudFog,
  CloudLightning,
  CloudRain,
  CloudSnow,
  CloudSun,
  Cloudy,
  Droplets,
  Sun,
  Wind,
} from '@lucide/vue'

const props = defineProps({
  tour: {
    type: Object,
    default: null,
  },
})

const weather = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')

const hasLocation = computed(() => {
  return props.tour?.mapX && props.tour?.mapY
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

async function fetchTourWeather(tour) {
  if (!tour?.mapX || !tour?.mapY) {
    weather.value = null
    errorMessage.value = '관광지 위치 정보가 없습니다.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const params = new URLSearchParams({
      latitude: tour.mapY,
      longitude: tour.mapX,
      current: 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
      timezone: 'Asia/Seoul',
    })

    const response = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`)

    if (!response.ok) {
      throw new Error('날씨 정보를 불러오지 못했습니다.')
    }

    const data = await response.json()
    const current = data.current

    weather.value = {
      temperature: Math.round(current.temperature_2m),
      humidity: current.relative_humidity_2m,
      windSpeed: Math.round(current.wind_speed_10m),
      weatherText: getWeatherText(current.weather_code),
      icon: getWeatherIcon(current.weather_code),
    }
  } catch (error) {
    weather.value = null
    errorMessage.value = error.message || '날씨 정보를 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}

watch(
  () => props.tour,
  (tour) => {
    fetchTourWeather(tour)
  },
  { immediate: true },
)
</script>

<template>
  <section class="tour-weather-card">
    <p class="eyebrow">현재 카드 지역 날씨</p>
    <h2>{{ tour?.name || '관광지를 선택해주세요' }}</h2>

    <p v-if="!tour" class="state-message">관광지 카드를 불러오는 중입니다.</p>
    <p v-else-if="isLoading" class="state-message">날씨 정보를 불러오는 중...</p>
    <p v-else-if="errorMessage" class="state-message error">{{ errorMessage }}</p>

    <div v-else-if="weather && hasLocation" class="weather-content">
      <div class="temperature">
        <div class="temperature-main">
          <component :is="weather.icon" class="weather-icon" :size="42" :stroke-width="2.2" />
          <strong>{{ weather.temperature }}°</strong>
        </div>
        <span>{{ weather.weatherText }}</span>
      </div>

      <div class="weather-detail">
        <span><Droplets :size="16" /> 습도 {{ weather.humidity }}%</span>
        <span><Wind :size="16" /> 풍속 {{ weather.windSpeed }}km/h</span>
      </div>
    </div>

    <p class="source">Weather: Open-Meteo</p>
  </section>
</template>

<style scoped>
.tour-weather-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  min-height: 260px;
  padding: 28px 22px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  color: #111827;
  background:
    radial-gradient(circle at 18% 18%, rgba(16, 185, 129, 0.12), transparent 34%),
    radial-gradient(circle at 84% 18%, rgba(59, 130, 246, 0.1), transparent 30%),
    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  text-align: center;
}

.eyebrow {
  position: absolute;
  top: 18px;
  left: 20px;
  margin: 0;
  color: #047857;
  font-size: 12px;
  font-weight: 800;
}

h2 {
  margin: 16px 0 18px;
  color: #111827;
  font-size: 32px;
  font-weight: 500;
  line-height: 1.2;
  word-break: keep-all;
}

.state-message {
  margin: 42px 0;
  color: #6b7280;
  text-align: center;
  font-weight: 700;
}

.state-message.error {
  color: #b91c1c;
}

.weather-content {
  display: grid;
  gap: 16px;
  justify-items: center;
}

.temperature {
  display: grid;
  gap: 8px;
  justify-items: center;
  min-width: min(100%, 230px);
  padding: 18px 18px 16px;
  border: 1px solid rgba(4, 120, 87, 0.1);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.06);
  backdrop-filter: blur(10px);
}

.temperature-main {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
}

.weather-icon {
  color: #047857;
  padding: 8px;
  border-radius: 18px;
  background: #ecfdf5;
}

.temperature strong {
  color: #111827;
  font-size: clamp(64px, 8vw, 96px);
  font-weight: 300;
  letter-spacing: -0.08em;
  line-height: 0.95;
}

.temperature span {
  color: #6b7280;
  font-size: 28px;
  font-weight: 700;
}

.weather-detail {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.weather-detail span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 13px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  color: #4b5563;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
  text-align: center;
  font-size: 13px;
  font-weight: 700;
}

.weather-detail svg {
  color: #047857;
}

.source {
  position: absolute;
  right: 16px;
  bottom: 12px;
  margin: 0;
  color: #9ca3af;
  font-size: 10px;
}
</style>
