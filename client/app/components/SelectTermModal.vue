<script setup lang="ts">
import * as v from 'valibot'
import type { FormSubmitEvent } from '@nuxt/ui'
import { useUserStore} from "~/stores/user";

const analysis = useAnalysis()
const userStore = useUserStore()

const terms = ref<string[]>(['Все'])
const isModalOpen = ref<boolean>(false)
const loading = ref<boolean>(false)

const openModal = () => isModalOpen.value = true

const closeModal = () => isModalOpen.value = false

const schema = v.object({
  selectTerm: v.pipe(v.string(), v.minLength(1, 'Выберите семестр из списка'))
})

type Schema = v.InferOutput<typeof schema>

const state = reactive({
  selectTerm: ''
})

const onSubmit = async (event: FormSubmitEvent<Schema>) => {
  loading.value = true
  const user = JSON.parse(sessionStorage.getItem('user')!)

  await analysis.analyze({
    username: user.username,
    password: user.password,
    term: event.data.selectTerm === 'Все' ? '' : event.data.selectTerm
  })

  loading.value = false
  closeModal()
}

onMounted(() => {
  const userTerms = userStore.user?.terms.map(String)

  if (Array.isArray(userTerms)) {
    terms.value.push(...userTerms)
  }
})
</script>

<template>
  <UButton label="Выбрать семестр" @click="openModal" class="cursor-pointer w-20 sm:w-fit" />
    <UModal v-model:open="isModalOpen" title="Выберите семестр/триместр для анализа">
      <template #body>
        <UForm :schema="schema" :state="state" @submit="onSubmit" class="space-y-4">
          <UFormField
              required
              label="Выберите доступный семестр"
              name="selectTerm"
          >
            <USelect v-model="state.selectTerm" :items="terms" class="w-full cursor-pointer" />
          </UFormField>

          <UButton :loading="loading" loading-icon="i-lucide-loader" type="submit" label="Анализ" class="flex justify-center items-center w-full cursor-pointer" />
        </UForm>
      </template>
    </UModal>
</template>
