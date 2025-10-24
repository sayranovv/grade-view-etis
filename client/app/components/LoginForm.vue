<script setup lang="ts">
import * as v from 'valibot'
import type {FormSubmitEvent} from '@nuxt/ui'
import type {LoginRequest} from "~/types/api";

const auth = useAuth()

const schema = v.object({
  username: v.pipe(v.string(), v.email('Некорректный email')),
  password: v.pipe(v.string(), v.minLength(1, 'Введите пароль'))
})

type Schema = v.InferOutput<typeof schema>

const state = reactive({
  username: '',
  password: '',
})

const showPassword = ref(false)
const authLoading = ref(false)

const toast = useToast()
const router = useRouter()

const handleLogin = async (credentials: LoginRequest) => {
  authLoading.value = true

  try {
    await auth.login(credentials)

    toast.add(
        { title: 'Успешный вход', color: 'success' }
    )

    await router.push('/')
  } catch (error: any) {

    toast.add(
        { title: 'Ошибка входа', description: 'Проверьте корректность введенных данных', color: 'error' }
    )

    console.error(error.message)
  } finally {
    authLoading.value = false
  }
}

const onSubmit = async (event: FormSubmitEvent<Schema>) => {
  await handleLogin(event.data)
}
</script>

<template>
  <div class="bg-neutral-950 py-8 px-10 rounded-2xl border border-neutral-800 min-w-80">
    <UForm :schema="schema" :state="state" @submit="onSubmit" class="space-y-7">
      <h1 class="text-xl font-bold text-center">Войдите в ЕТИС</h1>

      <div class="space-y-5 w-full">
        <UFormField required label="Email" name="username">
          <UInput v-model="state.username" placeholder="Введите email от ЕТИС" class="w-full" />
        </UFormField>

        <UFormField required label="Пароль" name="password">
          <UInput v-model="state.password"
                  placeholder="Введите пароль от ЕТИС"
                  :type="showPassword ? 'text' : 'password'"
                  :ui="{ trailing: 'pe-1' }"
                  class="w-full"
          >
            <template #trailing>
              <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showPassword ? 'i-lucide-eye' : 'i-lucide-eye-off'"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showPassword"
                  aria-controls="password"
                  @click="showPassword = !showPassword"
              />
            </template>
          </UInput>
        </UFormField>
      </div>

      <UButton label="Войти" type="submit" class="w-full flex justify-center items-center cursor-pointer" />
    </UForm>
  </div>
</template>