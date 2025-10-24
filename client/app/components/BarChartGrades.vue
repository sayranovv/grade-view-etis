<script lang="ts" setup>
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

const xFormatter = (i: number) => (props.data && props.data[i] ? props.data[i].subject : '')
const yFormatter = (tick: number) => tick.toString()
</script>

<template>
  <BarChart
      v-if="data && data.length"
      :data="data"
      :height="50 * data.length"
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