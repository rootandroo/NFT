import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import List from '../views/ListingRequests.vue'

const AssetList = () => import('../views/AssetList.vue')
const About = () => import('../views/About.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/:project/:drop?',
    name: 'AssetList',
    component: AssetList
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/list',
    name: 'List',
    component: List
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
