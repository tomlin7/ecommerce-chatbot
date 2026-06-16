"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import {
  LogOut,
  MessageCircle,
  Settings,
  ShoppingCart,
  User,
} from "lucide-react";
import Link from "next/link";

export function Header() {
  const { user, logout } = useAuth();
  const { t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center space-x-6">
          <Link href="/" className="flex items-center space-x-0.5">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-2xl">
                S
              </span>
            </div>
            <span className="font-bold text-xl">TORE</span>
          </Link>

          <nav className="hidden md:flex items-center space-x-6">
            <Link
              href="/products"
              className="text-sm font-medium hover:text-primary transition-colors"
            >
              {t('nav.products')}
            </Link>
            <Link
              href="/chat"
              className="text-sm font-medium hover:text-primary transition-colors"
            >
              {t('nav.aiAssistant')}
            </Link>
          </nav>
        </div>

        <div className="flex items-center space-x-3">
          <LanguageSwitcher />

          {user ? (
            <>
              <Button variant="ghost" size="icon" asChild>
                <Link href="/cart">
                  <ShoppingCart className="h-5 w-5" />
                </Link>
              </Button>

              <Button variant="ghost" size="icon" asChild className="md:hidden">
                <Link href="/chat">
                  <MessageCircle className="h-5 w-5" />
                </Link>
              </Button>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    className="relative h-8 w-8 rounded-full"
                  >
                    <Avatar className="h-8 w-8">
                      <AvatarFallback>
                        {user.name.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {user.name}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/profile">
                      <User className="mr-2 h-4 w-4" />
                      <span>{t('nav.profile')}</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/profile/preferences">
                      <Settings className="mr-2 h-4 w-4" />
                      <span>{t('nav.preferences')}</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={logout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>{t('nav.logout')}</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <div className="flex items-center space-x-2">
              <Button variant="ghost" asChild>
                <Link href="/login">{t('nav.login')}</Link>
              </Button>
              <Button asChild>
                <Link href="/register">{t('nav.register')}</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
