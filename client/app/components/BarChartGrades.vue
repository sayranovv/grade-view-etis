<script lang="ts" setup>
import { useWindowSize } from '@vueuse/core'

const props = defineProps<{
  data: {
    subject: string
    grade: number
  }[]
}>()

const categories = computed(() => ({
  grade: {
    name: 'Средний балл',
    color: '#22c55e',
  },
}))

const { width } = useWindowSize()

const chartHeight = computed(() => {
  if (!props.data?.length) return 300
  if (width.value < 600) return 90 * props.data.length
  if (width.value < 1000) return 80 * props.data.length
  return 50 * props.data.length
})

const xFormatter = (i: number) => (props.data && props.data[i] ? props.data[i].subject : '')
const yFormatter = (tick: number) => tick.toString()
</script>

<template>
  <BarChart
      v-if="data && data.length"
      :data="data"
      :height="chartHeight"
      :categories="categories"
      :y-axis="['grade']"
      :y-num-ticks="data.length"
      :radius="4"
      :x-grid-line="true"
      :y-formatter="xFormatter"
      :x-formatter="yFormatter"
      :legend-position="LegendPosition.Top"
      :hide-legend="false"
      :orientation="Orientation.Horizontal"
  />
</template>
