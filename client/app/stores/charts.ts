import { defineStore } from 'pinia'
import type {ChartData} from "~/types/api";

export const useChartsStore = defineStore('chartsStore', () => {
  const barData = ref<ChartData | null>(null)
  const lineData = ref<ChartData | null>(null)
  const loading = ref<boolean>(false)

  const setBarData = (data: ChartData) => barData.value = data
  const setLineData = (data: ChartData) => lineData.value = data
  const setLoading = (value: boolean) => loading.value = value

  const formattedBarData = computed(() => {
    if (!barData.value) return []

    return barData.value.labels.map((subject, index) => ({
      subject,
      grade: barData.value!.values[index] ?? 0
    }))
  })
  const formattedLineData = computed(() => {
    if (!lineData.value) return []

    return lineData.value.labels.map((term, index) => ({
      term,
      score: lineData.value!.values[index] ?? 0
    }))
  })

  return {
    barData,
    lineData,
    loading,
    setBarData,
    setLineData,
    setLoading,
    formattedBarData,
    formattedLineData
  }
})