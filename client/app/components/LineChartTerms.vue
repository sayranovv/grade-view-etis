<script setup lang="ts">
const props = defineProps<{
  data: {
    term: number
    score: number
  }[]
}>()

const categories = {
  score: {
    name: 'Средний балл за семестр',
    color: '#3b82f6',
  },
}

const xFormatter = (i: number) => (props.data && props.data[i] ? props.data[i].term : '')
</script>

<template>
    <LineChart
        v-if="data && data.length"
        :data="data"
        :categories="categories"
        :height="300"
        :xFormatter="xFormatter"
        xLabel="Семестр"
        yLabel="Средний балл"
    />
</template>