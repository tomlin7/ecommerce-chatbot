'use client'

import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { useLanguage } from '@/context/LanguageContext'
import { Send } from 'lucide-react'
import { useState } from 'react'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const { t } = useLanguage()
  const [message, setMessage] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <Textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={t('chat.inputPlaceholder')}
        className="min-h-[60px] resize-none"
        disabled={disabled}
      />
      <Button type="submit" size="icon" disabled={!message.trim() || disabled}>
        <Send className="h-4 w-4" />
      </Button>
    </form>
  )
}
