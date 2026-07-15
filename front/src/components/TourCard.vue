<script setup>
import { computed } from 'vue'

const props = defineProps({
  tour: {
    type: Object,
    required: true,
  },
})

const phoneLink = computed(() => {
  if (!props.tour.tel) return ''

  return String(props.tour.tel)
    .replace(/\s+/g, '')
    .replace(/[()]/g, '')
})
</script>

<template>
  <article class="tour-card">
    <div class="image-wrapper">
      <img
        v-if="tour.imageUrl"
        :src="tour.imageUrl"
        :alt="`${tour.name} 관광지 이미지`"
        class="tour-image"
        loading="lazy"
      />

      <div v-else class="image-placeholder">이미지가 없습니다</div>
    </div>

    <div class="tour-information">
      <p class="tour-category">서울 관광지</p>
      <h3 class="tour-name">{{ tour.name }}</h3>

      <dl class="tour-detail-list">
        <div class="tour-detail-row">
          <dt>
            <span class="detail-icon">⌖</span>
            <span>위치</span>
          </dt>
          <dd>{{ tour.address || '주소 정보 없음' }}</dd>
        </div>

        <div class="tour-detail-row">
          <dt>
            <span class="detail-icon">☎</span>
            <span>전화</span>
          </dt>
          <dd>
            <a v-if="tour.tel" :href="`tel:${phoneLink}`" class="phone-link">
              {{ tour.tel }}
            </a>
            <span v-else class="empty-information">전화번호 정보 없음</span>
          </dd>
        </div>
      </dl>

      <div v-if="tour.overview" class="overview-section">
        <div class="overview-header">
          <h4>관광지 소개</h4>
          <span>스크롤하여 전체 보기</span>
        </div>

        <div class="tour-overview" tabindex="0">
          {{ tour.overview }}
        </div>
      </div>

      <div class="tour-actions">
        <a
          v-if="tour.homepage"
          :href="tour.homepage"
          target="_blank"
          rel="noopener noreferrer"
          class="homepage-button"
        >
          <span>홈페이지 보기</span>
          <span class="homepage-arrow" aria-hidden="true">↗</span>
        </a>

        <div v-else class="homepage-button disabled">홈페이지 정보 없음</div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.tour-card {
  overflow: hidden;
  width: 100%;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  box-shadow: 0 12px 30px rgb(15 23 42 / 8%);
}

.image-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #f1f5f9;
  border-bottom: 1px solid #e2e8f0;
}

.tour-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: #8492a6;
  font-size: 14px;
}

.tour-information {
  padding: 24px;
}

.tour-category {
  margin: 0 0 7px;
  color: #047857;
  font-size: 13px;
  font-weight: 800;
}

.tour-name {
  margin: 0 0 20px;
  color: #172033;
  font-size: 25px;
  line-height: 1.35;
  word-break: keep-all;
}

.tour-detail-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 0;
}

.tour-detail-row {
  display: grid;
  grid-template-columns: 90px minmax(0, 1fr);
  min-height: 52px;
  padding: 10px 14px;
  background: #f7f9fc;
  border: 1px solid #edf1f6;
  border-radius: 11px;
}

.tour-detail-row dt,
.tour-detail-row dd {
  display: flex;
  align-items: center;
}

.tour-detail-row dt {
  gap: 7px;
  color: #334155;
  font-size: 14px;
  font-weight: 700;
}

.tour-detail-row dd {
  min-width: 0;
  margin: 0;
  color: #475569;
  font-size: 14px;
  line-height: 1.55;
  word-break: keep-all;
}

.detail-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 25px;
  height: 25px;
  color: #047857;
  background: #d1fae5;
  border-radius: 7px;
  font-size: 13px;
}

.phone-link {
  color: #047857;
  font-weight: 700;
  text-decoration: none;
}

.phone-link:hover {
  text-decoration: underline;
}

.empty-information {
  color: #94a3b8;
}

.overview-section {
  margin-top: 20px;
}

.overview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 9px;
}

.overview-header h4 {
  margin: 0;
  color: #334155;
  font-size: 14px;
}

.overview-header span {
  color: #94a3b8;
  font-size: 11px;
}

.tour-overview {
  max-height: 128px;
  padding: 14px 15px;
  overflow-y: auto;
  color: #5b6575;
  background: #f8fafc;
  border: 1px solid #e9eef5;
  border-radius: 11px;
  font-size: 14px;
  line-height: 1.75;
  white-space: pre-line;
  word-break: keep-all;
}

.tour-actions {
  margin-top: 20px;
}

.homepage-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  width: 100%;
  min-height: 50px;
  padding: 13px 20px;
  color: #ffffff;
  background: #111827;
  border-radius: 11px;
  font-size: 16px;
  font-weight: 800;
  text-decoration: none;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.homepage-button:hover {
  background: #047857;
  transform: translateY(-2px);
}

.homepage-button.disabled {
  color: #94a3b8;
  background: #eef2f7;
  cursor: default;
}

@media (max-width: 560px) {
  .tour-information {
    padding: 20px;
  }

  .tour-name {
    font-size: 22px;
  }

  .tour-detail-row {
    grid-template-columns: 78px minmax(0, 1fr);
    padding: 10px;
  }

  .detail-icon {
    display: none;
  }
}
</style>
