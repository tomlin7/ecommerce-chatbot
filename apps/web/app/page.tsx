"use client";

import { ProductGrid } from "@/components/products/ProductGrid";
import { Button } from "@/components/ui/button";
import { PixelAnimation } from "@/components/ui/PixelAnimation";
import { useLanguage } from "@/context/LanguageContext";
import api from "@/lib/api";
import { Product } from "@/types";
import { ArrowRight, Sprout, ShoppingBag } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function HomePage() {
  const { t } = useLanguage();
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedProducts();
  }, []);

  const fetchFeaturedProducts = async () => {
    try {
      const response = await api.get("/products/", {
        params: { limit: 8, min_rating: 4.5 },
      });
      if (response.data.success) {
        setFeaturedProducts(response.data.products);
      }
    } catch (error) {
      console.error("Failed to fetch featured products:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center overflow-hidden">
        <PixelAnimation className="z-0" opacity={1} speed={1} />
        <div className="absolute inset-0 bg-gradient-radial from-green-900 via-green-900/40 to-transparent z-5"></div>
        <div className="container max-w-4xl relative z-10">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-green-400 to-green-300 bg-clip-text text-transparent">
            {t('home.heroTitle')}
          </h1>
          <p className="text-xl text-foreground mb-8 max-w-2xl mx-auto">
            {t('home.heroSubtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild className="bg-green-600 hover:bg-green-700">
              <Link href="/products">
                <ShoppingBag className="mr-2 h-5 w-5" />
                {t('home.goToProducts')}
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/farms">
                <Sprout className="mr-2 h-5 w-5" />
                {t('home.ourFarmers')}
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="container px-4">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold mb-2">{t('home.seasonalTitle')}</h2>
            <p className="text-muted-foreground">{t('home.seasonalSubtitle')}</p>
          </div>
          <Button variant="outline" asChild>
            <Link href="/products">
              {t('home.allProducts')}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>

        <ProductGrid products={featuredProducts} loading={loading} />
      </section>

      {/* Why Choose Us Section */}
      <section className="container px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">{t('home.benefitsTitle')}</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            {t('home.benefitsSubtitle')}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <Sprout className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('home.farmToTable')}</h3>
            <p className="text-muted-foreground">{t('home.farmToTableDesc')}</p>
          </div>

          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('home.organicCert')}</h3>
            <p className="text-muted-foreground">{t('home.organicCertDesc')}</p>
          </div>

          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('home.supportLocal')}</h3>
            <p className="text-muted-foreground">{t('home.supportLocalDesc')}</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-background py-16 relative overflow-hidden">
        <PixelAnimation className="z-0" opacity={1} speed={1} />
        <div className="absolute inset-0 bg-gradient-radial from-green-900 via-green-900/30 to-transparent z-5"></div>
        <div className="container px-4 text-center relative z-10">
          <h2 className="text-3xl font-bold mb-4">{t('home.ctaTitle')}</h2>
          <p className="text-foreground mb-8 max-w-2xl mx-auto">
            {t('home.ctaSubtitle')}
          </p>
          <Button size="lg" asChild className="bg-green-600 hover:bg-green-700">
            <Link href="/products">
              <ShoppingBag className="h-5 w-5" />
              {t('home.startShopping')}
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
