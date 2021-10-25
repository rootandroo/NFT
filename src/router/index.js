import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const AssetList = () => import('../views/AssetList.vue')
const About = () => import('../views/About.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/:project',
    name: 'AssetList',
    component: AssetList
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
