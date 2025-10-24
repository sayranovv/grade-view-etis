<script setup lang="ts">
import { LucideAreaChart } from 'lucide-vue-next'

</script>
<template>
  <UHeader title="Grade View ETIS">
    <template #left>
      <LucideAreaChart class="size-8" />
      <h1 class="text-xl font-bold">Grade View ETIS</h1>
    </template>
    <template #right>
      <SelectTermModal/>
      <LogoutConfirmationModal />
    </template>
  </UHeader>
  <div class="my-8">
    <slot />
  </div>
  <UFooter />
</template>