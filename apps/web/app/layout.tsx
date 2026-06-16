import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { Toaster } from "@/components/ui/sonner";
import { AuthProvider } from "@/context/AuthContext";
import { LanguageProvider } from "@/context/LanguageContext";
import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Фермерский магазин — свежие продукты",
  description:
    "Откройте для себя свежие фермерские продукты с доставкой прямо к вашему столу. Поддержите местных фермеров и наслаждайтесь лучшими органическими и сезонными продуктами.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false}
          disableTransitionOnChange
        >
          <LanguageProvider>
            <AuthProvider>
              <div className="min-h-screen flex flex-col">
                <Header />
                <main className="flex-1 overflow-auto">{children}</main>
                <Footer />
              </div>
              <Toaster />
            </AuthProvider>
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
