import type {AnalysisResponse, FileType} from "~/types/api"
import { saveAs } from 'file-saver'

export const useAnalysis = () => {
  const chartsStore = useChartsStore()
  const userStore = useUserStore()
  const config = useRuntimeConfig()

  const analyze = async (params: { username: string; password: string; term: string }) => {
    userStore.setSelectedTerm( params.term )

    chartsStore.setLoading(true)

    try {
      const data = await $fetch<AnalysisResponse>(`${config.public.apiBase || 'http://localhost:8000'}/api/analyze`, {
        method: 'POST',
        body: params,
      })

      if (data.success) {
        chartsStore.setBarData(data.bar_data)
        chartsStore.setLineData(data.line_data)

        return data
      } else {
        throw new Error(data.message || 'Ошибка анализа')
      }
    } catch (error) {
      console.error('Ошибка анализа:', error)
      throw error
    } finally {
      chartsStore.setLoading(false)
    }
  }

  const downloadFile = async (fileType: string) => {
    try {
      const response = await $fetch<Blob>(`${config.public.apiBase || 'http://localhost:8000'}/download/${fileType}`, {
        method: 'GET',
        query: {
          username: userStore.user?.username,
          term: userStore.selectedTerm || ''
        },
        responseType: 'blob'
      })

      const blob = new Blob([response])
      const fileName = fileType === 'csv' ? 'grades.csv' :
        fileType === 'xlsx' ? 'grades.xlsx' :
          `${fileType}.png`

      saveAs(blob, fileName)
    } catch (err) {
      console.error('Ошибка при скачивании файла:', err)
      alert('Файл не найден. Сначала выполните анализ данных.')
    }
  }

  return {
    analyze,
    downloadFile,
  }
}
