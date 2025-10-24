<script setup lang="ts">
const auth = useAuth()
const router = useRouter()
const isOpen = ref(false)
const loading = ref(false)

const closeModal = () => isOpen.value = false

const logoutHandler = async () => {
  loading.value = true

  setTimeout(() => {
    auth.logout()
    router.push('/login')

    loading.value = false
  }, 800)


}
</script>

<template>
  <UModal v-model:open="isOpen">
    <UButton class="cursor-pointer" color="error" label="Выйти" leading-icon="i-lucide-log-out" />

    <template #content>
      <div class="p-8">
        <p class="text-lg text-center">Вы уверены, что хотите выйти из аккаунта ЕТИС?</p>

        <div class="grid grid-cols-2 gap-2 mt-4">
          <UButton class="flex justify-center cursor-pointer" label="Отмена" variant="soft" @click="closeModal" />
          <UButton
              :loading="loading"
              loading-icon="i-lucide-loader"
              class="flex justify-center items-center cursor-pointer"
              color="error"
              label="Выйти"
              @click="logoutHandler"
               />
        </div>
      </div>
    </template>
  </UModal>
</template>