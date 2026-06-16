'use client'

import { createContext, ReactNode, useCallback, useContext, useEffect, useState } from 'react'
import { kk } from '@/lib/translations/kk'
import { ru } from '@/lib/translations/ru'

export type Language = 'ru' | 'kk'

const translations: Record<Language, Record<string, unknown>> = {
  ru: ru as unknown as Record<string, unknown>,
  kk: kk as unknown as Record<string, unknown>,
}

function getNestedValue(obj: Record<string, unknown>, path: string): string {
  const result = path.split('.').reduce<unknown>((acc, key) => {
    if (acc && typeof acc === 'object') return (acc as Record<string, unknown>)[key]
    return undefined
  }, obj)
  return typeof result === 'string' ? result : path
}

interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string, params?: Record<string, string | number>) => string
}

const LanguageContext = createContext<LanguageContextType | null>(null)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>('ru')

  useEffect(() => {
    const saved = localStorage.getItem('app-language') as Language | null
    if (saved === 'ru' || saved === 'kk') {
      setLanguageState(saved)
    }
  }, [])

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang)
    localStorage.setItem('app-language', lang)
  }, [])

  const t = useCallback(
    (key: string, params?: Record<string, string | number>): string => {
      let value = getNestedValue(translations[language], key)
      if (params) {
        Object.entries(params).forEach(([k, v]) => {
          value = value.replace(`{${k}}`, String(v))
        })
      }
      return value
    },
    [language]
  )

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage(): LanguageContextType {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used inside <LanguageProvider>')
  return ctx
}
