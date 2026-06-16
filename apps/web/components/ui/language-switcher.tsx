'use client'

import { useLanguage } from '@/context/LanguageContext'

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage()

  return (
    <div className="flex items-center rounded-md border border-border overflow-hidden text-xs font-semibold">
      <button
        onClick={() => setLanguage('ru')}
        className={`px-2.5 py-1 transition-colors ${
          language === 'ru'
            ? 'bg-primary text-primary-foreground'
            : 'text-muted-foreground hover:text-foreground hover:bg-muted'
        }`}
        aria-label="Русский язык"
      >
        РУС
      </button>
      <button
        onClick={() => setLanguage('kk')}
        className={`px-2.5 py-1 transition-colors ${
          language === 'kk'
            ? 'bg-primary text-primary-foreground'
            : 'text-muted-foreground hover:text-foreground hover:bg-muted'
        }`}
        aria-label="Қазақ тілі"
      >
        ҚАЗ
      </button>
    </div>
  )
}
