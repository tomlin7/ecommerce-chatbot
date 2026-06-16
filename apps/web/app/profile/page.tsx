'use client'

import { useAuth } from '@/context/AuthContext'
import { useLanguage } from '@/context/LanguageContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { User, Settings, ShoppingBag, MessageCircle } from 'lucide-react'
import { formatDate } from '@/lib/utils'
import Link from 'next/link'

export default function ProfilePage() {
  const { user } = useAuth()
  const { t } = useLanguage()

  if (!user) {
    return (
      <div className="container py-8">
        <Card className="max-w-md mx-auto text-center">
          <CardContent className="pt-6">
            <User className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <h2 className="text-xl font-semibold mb-2">{t('profile.loginRequired')}</h2>
            <p className="text-muted-foreground mb-4">{t('profile.loginMessage')}</p>
            <Button asChild>
              <Link href="/login">{t('profile.login')}</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{t('profile.title')}</h1>
        <p className="text-muted-foreground">{t('profile.subtitle')}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Info */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('profile.accountInfo.title')}</CardTitle>
              <CardDescription>{t('profile.accountInfo.desc')}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-muted-foreground">
                    {t('profile.accountInfo.fullName')}
                  </label>
                  <p className="text-lg">{user.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">
                    {t('profile.accountInfo.email')}
                  </label>
                  <p className="text-lg">{user.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">
                    {t('profile.accountInfo.memberSince')}
                  </label>
                  <p className="text-lg">{formatDate(user.created_at)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">
                    {t('profile.accountInfo.status')}
                  </label>
                  <p className="text-lg">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      {t('profile.accountInfo.active')}
                    </span>
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('profile.preferences.title')}</CardTitle>
              <CardDescription>{t('profile.preferences.desc')}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  {t('profile.preferences.favoriteCategories')}
                </label>
                <div className="flex flex-wrap gap-2 mt-1">
                  {user.preferences.favoriteCategories.length > 0 ? (
                    user.preferences.favoriteCategories.map((category, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary"
                      >
                        {category}
                      </span>
                    ))
                  ) : (
                    <p className="text-muted-foreground">
                      {t('profile.preferences.noPreferences')}
                    </p>
                  )}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  {t('profile.preferences.priceRange')}
                </label>
                <p className="text-lg">
                  ${user.preferences.priceRange[0]} - ${user.preferences.priceRange[1]}
                </p>
              </div>

              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  {t('profile.preferences.favoriteBrands')}
                </label>
                <div className="flex flex-wrap gap-2 mt-1">
                  {user.preferences.favoriteBrands.length > 0 ? (
                    user.preferences.favoriteBrands.map((brand, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-secondary text-secondary-foreground"
                      >
                        {brand}
                      </span>
                    ))
                  ) : (
                    <p className="text-muted-foreground">
                      {t('profile.preferences.noBrands')}
                    </p>
                  )}
                </div>
              </div>

              <Button asChild>
                <Link href="/profile/preferences">
                  <Settings className="mr-2 h-4 w-4" />
                  {t('profile.preferences.update')}
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('profile.quickActions.title')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start" asChild>
                <Link href="/cart">
                  <ShoppingBag className="mr-2 h-4 w-4" />
                  {t('profile.quickActions.viewCart')}
                </Link>
              </Button>

              <Button variant="outline" className="w-full justify-start" asChild>
                <Link href="/chat">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  {t('profile.quickActions.aiAssistant')}
                </Link>
              </Button>

              <Button variant="outline" className="w-full justify-start" asChild>
                <Link href="/profile/preferences">
                  <Settings className="mr-2 h-4 w-4" />
                  {t('profile.quickActions.settings')}
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('profile.stats.title')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <p className="text-2xl font-bold">0</p>
                <p className="text-sm text-muted-foreground">{t('profile.stats.orders')}</p>
              </div>

              <Separator />

              <div className="text-center">
                <p className="text-2xl font-bold">$0.00</p>
                <p className="text-sm text-muted-foreground">{t('profile.stats.totalSpent')}</p>
              </div>

              <Separator />

              <div className="text-center">
                <p className="text-2xl font-bold">0</p>
                <p className="text-sm text-muted-foreground">{t('profile.stats.chatSessions')}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
