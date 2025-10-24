<script setup lang="ts">
import { LucideAreaChart } from 'lucide-vue-next'

</script>
<template>
  <UContainer>
    <div class="py-4 flex items-center justify-between border-b border-neutral-700">
      <div class="flex items-center gap-2">
        <LucideAreaChart class="size-8" />
        <h1 class="text-lg sm:text-xl font-bold leading-5">Grade View ETIS</h1>
      </div>
      <div class="flex items-center gap-2">
        <SelectTermModal />
        <LogoutConfirmationModal />
      </div>
    </div>
  </UContainer>

  <div class="my-8">
    <slot />
  </div>
  <UFooter />
</template>
