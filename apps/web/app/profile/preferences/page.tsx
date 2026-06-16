'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/context/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Slider } from '@/components/ui/slider'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { UserPreferences } from '@/types'
import { formatPrice } from '@/lib/utils'
import api from '@/lib/api'
import { X } from 'lucide-react'
import Link from 'next/link'

export default function PreferencesPage() {
  const { user, updatePreferences } = useAuth()
  const [preferences, setPreferences] = useState<UserPreferences>({
    favoriteCategories: [],
    priceRange: [0, 2000],
    favoriteBrands: []
  })
  const [categories, setCategories] = useState<string[]>([])
  const [brands, setBrands] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      setPreferences(user.preferences)
    }
    fetchCategories()
    fetchBrands()
  }, [user])

  const fetchCategories = async () => {
    try {
      const response = await api.get('/products/categories')
      if (response.data.success) {
        const categoryNames = response.data.categories.map((cat: any) => cat.category)
        setCategories(categoryNames)
      }
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const fetchBrands = async () => {
    try {
      const response = await api.get('/products/brands')
      if (response.data.success) {
        setBrands(response.data.brands)
      }
    } catch (error) {
      console.error('Failed to fetch brands:', error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    const success = await updatePreferences(preferences)
    setLoading(false)
  }

  const addCategory = (category: string) => {
    if (!preferences.favoriteCategories.includes(category)) {
      setPreferences(prev => ({
        ...prev,
        favoriteCategories: [...prev.favoriteCategories, category]
      }))
    }
  }

  const removeCategory = (category: string) => {
    setPreferences(prev => ({
      ...prev,
      favoriteCategories: prev.favoriteCategories.filter(c => c !== category)
    }))
  }

  const addBrand = (brand: string) => {
    if (!preferences.favoriteBrands.includes(brand)) {
      setPreferences(prev => ({
        ...prev,
        favoriteBrands: [...prev.favoriteBrands, brand]
      }))
    }
  }

  const removeBrand = (brand: string) => {
    setPreferences(prev => ({
      ...prev,
      favoriteBrands: prev.favoriteBrands.filter(b => b !== brand)
    }))
  }

  if (!user) {
    return (
      <div className="container py-8">
        <Card className="max-w-md mx-auto text-center">
          <CardContent className="pt-6">
            <h2 className="text-xl font-semibold mb-2">Пожалуйста, войдите</h2>
            <p className="text-muted-foreground mb-4">
              Вам нужно войти в систему, чтобы управлять предпочтениями.
            </p>
            <Button asChild>
              <Link href="/login">Войти</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Предпочтения покупок</h1>
        <p className="text-muted-foreground">
          Настройте свой опыт покупок для лучших рекомендаций
        </p>
      </div>

      <div className="max-w-2xl space-y-6">
        {/* Favorite Categories */}
        <Card>
          <CardHeader>
            <CardTitle>Любимые категории</CardTitle>
            <CardDescription>
              Выберите категории, которые вам интересны больше всего
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Добавить категорию</Label>
              <Select onValueChange={addCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Выберите категорию" />
                </SelectTrigger>
                <SelectContent>
                  {categories
                    .filter(cat => !preferences.favoriteCategories.includes(cat))
                    .map((category) => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex flex-wrap gap-2">
              {preferences.favoriteCategories.map((category) => (
                <Badge key={category} variant="secondary" className="flex items-center gap-1">
                  {category}
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-auto p-0 hover:bg-transparent"
                    onClick={() => removeCategory(category)}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Price Range */}
        <Card>
          <CardHeader>
            <CardTitle>Диапазон цен</CardTitle>
            <CardDescription>
              Установите предпочитаемый диапазон цен для рекомендаций товаров
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              <Slider
                value={preferences.priceRange}
                onValueChange={(value) => setPreferences(prev => ({
                  ...prev,
                  priceRange: [value[0], value[1]]
                }))}
                max={3000}
                min={0}
                step={50}
                className="w-full"
              />
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>{formatPrice(preferences.priceRange[0])}</span>
                <span>{formatPrice(preferences.priceRange[1])}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Favorite Brands */}
        <Card>
          <CardHeader>
            <CardTitle>Любимые бренды</CardTitle>
            <CardDescription>
              Выберите бренды, которые вы предпочитаете для персонализированных рекомендаций
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Добавить бренд</Label>
              <Select onValueChange={addBrand}>
                <SelectTrigger>
                  <SelectValue placeholder="Выберите бренд" />
                </SelectTrigger>
                <SelectContent>
                  {brands
                    .filter(brand => !preferences.favoriteBrands.includes(brand))
                    .map((brand) => (
                      <SelectItem key={brand} value={brand}>
                        {brand}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex flex-wrap gap-2">
              {preferences.favoriteBrands.map((brand) => (
                <Badge key={brand} variant="outline" className="flex items-center gap-1">
                  {brand}
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-auto p-0 hover:bg-transparent"
                    onClick={() => removeBrand(brand)}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end space-x-4">
          <Button variant="outline" asChild>
            <Link href="/profile">Отмена</Link>
          </Button>
          <Button onClick={handleSave} disabled={loading}>
            {loading ? 'Сохранение...' : 'Сохранить предпочтения'}
          </Button>
        </div>
      </div>
    </div>
  )
}