import { useUserStore } from "~/stores/user"

export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useUserStore()

  if (!userStore.user) {
    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }

  if (userStore.user && to.path === '/login') {
    return navigateTo('/')
  }
})