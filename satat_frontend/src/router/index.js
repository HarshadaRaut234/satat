import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import MapView from '@/components/MapView.vue'
import DecodeView from '@/components/DecodeView.vue'

const routes = [
    {
        path: '/',
        name: 'HomeView',
        component: HomeView
    },
  {
    path: '/map',
    name: 'MapView',
    component: MapView
  },
  {
    path: '/decode',
    name: 'DecodeView',
    component: DecodeView
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


export default router