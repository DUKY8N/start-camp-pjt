import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BoardView from '../views/BoardView.vue'
import BoardDetailView from '../views/BoardDetailView.vue'
import BoardEditView from '../views/BoardEditView.vue'
import BoardWriteView from '../views/BoardWriteView.vue'
import ChatbotView from '../views/ChatbotView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/board',
      name: 'board',
      component: BoardView,
    },
    {
      path: '/board/write',
      name: 'board-write',
      component: BoardWriteView,
    },
    {
      path: '/board/:id/edit',
      name: 'board-edit',
      component: BoardEditView,
    },
    {
      path: '/board/:id',
      name: 'board-detail',
      component: BoardDetailView,
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatbotView,
    },
  ],
})

export default router
