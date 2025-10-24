export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  success: boolean
  terms: number[]
}

export interface AnalyseRequest {
  username: string
  password: string
  terms: string
}

export interface AnalyseResponse {
  success: boolean
  bar_data: any
  line_data: any
}

export interface ChartData {
  labels: number[]
  values: number[]
}

export interface AnalysisResponse {
  success: boolean
  message: string
  bar_data: ChartData
  line_data: ChartData
}

export interface User {
  username: string
  password: string
  terms: number[]
}

export type FileType = 'csv' | 'xlsx' | 'avg_grades' | 'term_dynamics'

