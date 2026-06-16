"use client";

import { Separator } from "@/components/ui/separator";
import { useLanguage } from "@/context/LanguageContext";
import Link from "next/link";

export function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="border-t bg-background flex-shrink-0">
      <div className="container py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <div className="flex items-center space-x-0.5">
              <div className="h-6 w-6 rounded bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-xl">
                  S
                </span>
              </div>
              <span className="font-bold">TORE</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {t('footer.description')}
            </p>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">{t('footer.productsTitle')}</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/products?category=овощи" className="hover:text-foreground">
                  {t('footer.vegsAndFruits')}
                </Link>
              </li>
              <li>
                <Link href="/products?category=молочные продукты" className="hover:text-foreground">
                  {t('footer.dairy')}
                </Link>
              </li>
              <li>
                <Link href="/products?category=мясо" className="hover:text-foreground">
                  {t('footer.meat')}
                </Link>
              </li>
              <li>
                <Link href="/products?is_seasonal=true" className="hover:text-foreground">
                  {t('footer.seasonal')}
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">{t('footer.supportTitle')}</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/chat" className="hover:text-foreground">
                  {t('footer.aiAssistant')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.helpCenter')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.contactUs')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.returns')}
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">{t('footer.companyTitle')}</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.about')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.privacy')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.terms')}
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  {t('footer.careers')}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <Separator className="my-6" />

        <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-muted-foreground">
          <p>{t('footer.copyright')}</p>
          <p>{t('footer.builtWith')}</p>
        </div>
      </div>
    </footer>
  );
}
