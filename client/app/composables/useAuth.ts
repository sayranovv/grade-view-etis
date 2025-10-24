import {useUserStore} from "~/stores/user";

export const useAuth = () => {
  const store = useUserStore()

  const login = async (credentials: {username: string, password: string}) => {
    const { data, error } = await useFetch('http://localhost:8000/api/login', {
      method: 'POST',
      body: credentials
    })

    if (error.value) throw error.value

    store.setUser({
      ...credentials,
      terms: data.value.terms
    })

    return data.value
  }

  const logout = () => {
    store.deleteUser()
  }

  return {
    login,
    logout
  }

}
