<script setup lang="ts">
import {useChartsStore} from "~/stores/charts";
import type {FileType} from "~/types/api";

const analysis = useAnalysis()
const chartsStore = useChartsStore()

const handleDownload = (fileType: FileType) => analysis.downloadFile(fileType)
</script>

<template>
  <UContainer class="space-y-8" v-if="chartsStore.barData && chartsStore.lineData">
    <section class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="p-6 space-y-4 rounded-2xl border border-neutral-800 bg-neutral-950">
        <h2 class="text-center text-lg font-semibold">Динамика по семестрам</h2>
        <LineChartTerms :data="chartsStore.formattedLineData" />
      </div>

      <div class="flex flex-col h-full justify-between gap-2">
        <UButton class="flex justify-center items-center h-full rounded-2xl text-md cursor-pointer" variant="soft" label="Скачать CSV" @click="handleDownload('csv')" />
        <UButton class="flex justify-center items-center h-full rounded-2xl text-md cursor-pointer" variant="soft" label="Скачать XLSX" @click="handleDownload('xlsx')" />
        <UButton class="flex justify-center items-center h-full rounded-2xl text-md cursor-pointer" color="primary" label="Скачать график средних баллов" @click="handleDownload('avg_grades')" />
        <UButton class="flex justify-center items-center h-full rounded-2xl text-md cursor-pointer" color="secondary" label="Скачать график динамики по семестрам" @click="handleDownload('term_dynamics')" />
      </div>
    </section>

    <div class="p-6 space-y-4 rounded-2xl border border-neutral-800 bg-neutral-950">
    <BarChartGrades :data="chartsStore.formattedBarData" />
    </div>
  </UContainer>
</template>