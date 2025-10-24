import {defineStore} from "pinia";
import type {User} from "~/types/api";

export const useUserStore = defineStore('userStore', () => {
  const user = ref<User | null>(null)
  const selectedTerm = ref<string | null>(null)
  const isAuthenticated = computed(() => !!user.value)

  const setUser = (newUser: User) => {
    user.value = newUser
    sessionStorage.setItem('user', JSON.stringify(user.value))
  }

  const setSelectedTerm = (term: string | number) => {
    selectedTerm.value = term.toString()
  }

  const deleteUser = () => {
    user.value = null
    sessionStorage.removeItem('user')
  }

  return {
    user,
    selectedTerm,
    isAuthenticated,
    setUser,
    setSelectedTerm,
    deleteUser
  }
})