<script setup>
import {useUserStore} from "~/stores/user.js";

useHead({
  htmlAttrs: {
    class: 'dark',
  },
})

const store = useUserStore()

onMounted(() => {
  const saved = sessionStorage.getItem('user')

  if (saved) {
    store.user = JSON.parse(saved)
  }
})
</script>

<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage/>
    </NuxtLayout>
  </UApp>
</template>