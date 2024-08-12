import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../views/HomePage.vue'
import PartChangeover from '@/views/PartChangeover.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/part-changeover',
    name: 'PartChangeOver',
    component: PartChangeover
  },
  // routes อื่นๆ ถ้ามี
]

const router = new VueRouter({
  routes
})

export default router