"use client";

import { ChatInput } from "@/components/chat/ChatInput";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import api from "@/lib/api";
import { generateSessionId } from "@/lib/utils";
import { ChatSession, ChatMessage as Message } from "@/types";
import { Bot, Plus, Trash2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

export default function ChatPage() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [showSessions, setShowSessions] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const sessionsTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const makeWelcomeMessage = (sessionId: string): Message => ({
    id: "welcome",
    chatSessionId: sessionId,
    content: t('chat.welcomeMessage'),
    isBot: true,
    type: "text",
    products: [],
    extraData: {},
    timestamp: new Date().toISOString(),
  });

  useEffect(() => {
    if (user) {
      fetchSessions();
    } else {
      const sessionId = generateSessionId();
      setCurrentSessionId(sessionId);
      if (messages.length === 0) {
        setMessages([makeWelcomeMessage(sessionId)]);
      }
    }
  }, [user]);

  useEffect(() => {
    if (currentSessionId && user) {
      fetchChatHistory();
    }
  }, [currentSessionId, user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (scrollAreaRef.current) {
      setTimeout(() => {
        scrollAreaRef.current!.scrollTop = scrollAreaRef.current!.scrollHeight;
      }, 100);
    }
  };

  const fetchSessions = async () => {
    if (!user) return;
    setLoadingSessions(true);
    try {
      const response = await api.get("/chat/sessions");
      if (response.data.success) {
        setSessions(response.data.sessions);
        if (response.data.sessions.length > 0 && !currentSessionId) {
          setCurrentSessionId(response.data.sessions[0].id);
        } else if (response.data.sessions.length === 0) {
          createNewSession();
        }
      }
    } catch (error) {
      console.error("Failed to fetch sessions:", error);
    } finally {
      setLoadingSessions(false);
    }
  };

  const fetchChatHistory = async () => {
    if (!currentSessionId) return;
    try {
      const response = await api.get(`/chat/history/${currentSessionId}`);
      if (response.data.success && response.data.history) {
        const sanitizedHistory = response.data.history.map((message: any) => {
          let products = [];
          if (Array.isArray(message.products)) {
            products = message.products.filter((p: any) => p && p.id);
          }
          if (
            products.length === 0 &&
            message.productDetails &&
            Array.isArray(message.productDetails)
          ) {
            products = message.productDetails.filter((p: any) => p && p.id);
          }
          return { ...message, products };
        });
        setMessages(sanitizedHistory);
      } else {
        setMessages([]);
      }
    } catch (error) {
      if ((error as any).response?.status === 404) {
        setMessages([makeWelcomeMessage(currentSessionId)]);
      } else {
        setMessages([]);
      }
    }
  };

  const createNewSession = () => {
    const sessionId = generateSessionId();
    setCurrentSessionId(sessionId);
    setMessages([makeWelcomeMessage(sessionId)]);
    if (user) {
      fetchSessions();
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await api.delete(`/chat/sessions/${sessionId}`);
      setSessions(sessions.filter((s) => s.id !== sessionId));
      if (sessionId === currentSessionId) {
        if (sessions.length > 1) {
          const remaining = sessions.filter((s) => s.id !== sessionId);
          setCurrentSessionId(remaining[0].id);
        } else {
          createNewSession();
        }
      }
      toast(t('chat.sessionDeleted'));
    } catch {
      toast.error(t('chat.deleteError'));
    }
  };

  const sendMessage = async (content: string) => {
    if (!currentSessionId) return;
    const userMessage: Message = {
      id: Date.now().toString(),
      chatSessionId: currentSessionId,
      content,
      isBot: false,
      type: "text",
      products: [],
      extraData: {},
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    try {
      const response = await api.post("/chat/message", {
        message: content,
        session_id: currentSessionId,
      });
      if (response.data.success) {
        setMessages((prev) => [...prev, response.data.response]);
        if (user) fetchSessions();
      }
    } catch {
      toast.error(t('chat.sendError'));
    } finally {
      setLoading(false);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!user) return;
    if (e.clientX <= 50) {
      setShowSessions(true);
      if (sessionsTimeoutRef.current) {
        clearTimeout(sessionsTimeoutRef.current);
        sessionsTimeoutRef.current = null;
      }
    }
  };

  const handleMouseEnterSessions = () => {
    if (!user) return;
    setShowSessions(true);
    if (sessionsTimeoutRef.current) {
      clearTimeout(sessionsTimeoutRef.current);
      sessionsTimeoutRef.current = null;
    }
  };

  const handleMouseLeaveSessions = () => {
    if (!user) return;
    sessionsTimeoutRef.current = setTimeout(() => setShowSessions(false), 500);
  };

  useEffect(() => {
    return () => {
      if (sessionsTimeoutRef.current) clearTimeout(sessionsTimeoutRef.current);
    };
  }, []);

  return (
    <div className="flex-1 flex flex-col relative" onMouseMove={handleMouseMove}>
      {/* Floating Sessions Panel */}
      {user && (
        <div
          className={`fixed top-0 left-0 h-full w-80 z-50 transition-transform duration-300 ease-in-out ${
            showSessions ? "translate-x-0" : "-translate-x-full"
          }`}
          onMouseEnter={handleMouseEnterSessions}
          onMouseLeave={handleMouseLeaveSessions}
        >
          <Card className="h-full chat-card flex flex-col shadow-xl border-r">
            <CardHeader className="pb-3 flex-shrink-0">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{t('chat.sessionsTitle')}</CardTitle>
                <Button size="sm" onClick={createNewSession}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="p-0 flex-1 min-h-0 overflow-hidden">
              <ScrollArea className="h-full">
                <div className="space-y-2 p-4">
                  {loadingSessions ? (
                    <div className="text-center text-muted-foreground">
                      {t('chat.loading')}
                    </div>
                  ) : sessions.length === 0 ? (
                    <div className="text-center text-muted-foreground">
                      {t('chat.noSessions')}
                    </div>
                  ) : (
                    sessions.map((session) => (
                      <div
                        key={session.id}
                        className={`p-3 rounded-lg border border-muted cursor-pointer hover:bg-muted transition-colors ${
                          session.id === currentSessionId
                            ? "bg-muted border-primary"
                            : ""
                        }`}
                        onClick={() => {
                          setCurrentSessionId(session.id);
                          setMessages([]);
                          setShowSessions(false);
                        }}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate">
                              {t('chat.session')} {session.id.slice(-8)}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {t('chat.messagesCount', { count: session.messageCount })}
                            </p>
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteSession(session.id);
                            }}
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="container py-4 flex-1 flex flex-col min-h-0">
        <Card className="flex-1 flex flex-col">
          <CardHeader className="pb-3 flex-shrink-0">
            <CardTitle className="flex items-center gap-2">
              <div className="flex items-center space-x-1">
                <span className="font-bold text-xl">{t('chat.title')}</span>
                <Bot className="h-5 w-5" />
              </div>
              {user && (
                <span className="text-xs border-2 border-dashed border-blue-200/30 px-2 py-1 rounded-full ml-auto">
                  {t('chat.hoverHint')}
                </span>
              )}
            </CardTitle>
          </CardHeader>

          <CardContent className="flex-1 flex flex-col p-0 chat-container">
            <div className="chat-messages p-4" ref={scrollAreaRef}>
              <div className="space-y-6 pb-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                {loading && (
                  <div className="flex gap-3">
                    <div className="h-8 w-8 rounded-full bg-muted animate-pulse" />
                    <div className="flex-1">
                      <div className="h-4 bg-muted rounded animate-pulse mb-2" />
                      <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="p-4 border-t bg-background">
              <ChatInput onSendMessage={sendMessage} disabled={loading} />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
