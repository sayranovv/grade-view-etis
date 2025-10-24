/// <reference types="nuxt/schema" />

interface ImportMetaEnv {
  readonly NUXT_PUBLIC_API_BASE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
