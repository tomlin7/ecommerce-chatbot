"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import api from "@/lib/api";
import { formatPrice } from "@/lib/utils";
import { CartItem } from "@/types";
import { Minus, Plus, ShoppingBag, Trash2 } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "sonner";

export default function CartPage() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchCart();
    } else {
      setLoading(false);
    }
  }, [user]);

  const fetchCart = async () => {
    if (!user) return;
    try {
      const response = await api.get(`/cart/${user.id}`);
      setCartItems(response.data);
    } catch {
      toast.error(t('cart.loadError'));
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId: string, newQuantity: number) => {
    if (newQuantity < 1) {
      await removeItem(itemId);
      return;
    }
    try {
      await api.put("/cart/update", {
        user_id: user!.id,
        item_id: itemId,
        quantity: newQuantity,
      });
      setCartItems(
        cartItems.map((item) =>
          item.id === itemId ? { ...item, quantity: newQuantity } : item
        )
      );
      toast(t('cart.updated'));
    } catch {
      toast.error(t('cart.updateError'));
    }
  };

  const removeItem = async (itemId: string) => {
    try {
      await api.delete("/cart/remove", {
        data: { user_id: user!.id, item_id: itemId },
      });
      setCartItems(cartItems.filter((item) => item.id !== itemId));
      toast(t('cart.removed'));
    } catch {
      toast.error(t('cart.removeError'));
    }
  };

  const getTotalPrice = () =>
    cartItems.reduce((total, item) => total + (item.product?.price || 0) * item.quantity, 0);

  const getTotalItems = () =>
    cartItems.reduce((total, item) => total + item.quantity, 0);

  if (!user) {
    return (
      <div className="container py-8">
        <Card className="max-w-md mx-auto text-center">
          <CardContent className="pt-6">
            <ShoppingBag className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <h2 className="text-xl font-semibold mb-2">{t('cart.loginRequired')}</h2>
            <p className="text-muted-foreground mb-4">{t('cart.loginMessage')}</p>
            <Button asChild>
              <Link href="/login">{t('cart.login')}</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/4" />
          <div className="h-64 bg-muted rounded" />
        </div>
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="container py-8">
        <Card className="max-w-md mx-auto text-center">
          <CardContent className="pt-6">
            <ShoppingBag className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <h2 className="text-xl font-semibold mb-2">{t('cart.empty')}</h2>
            <p className="text-muted-foreground mb-4">{t('cart.emptyMessage')}</p>
            <Button asChild>
              <Link href="/products">{t('cart.goToProducts')}</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{t('cart.title')}</h1>
        <p className="text-muted-foreground">
          {t('cart.itemsCount', { count: getTotalItems() })}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>{t('cart.cartItems')}</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t('cart.product')}</TableHead>
                    <TableHead>{t('cart.price')}</TableHead>
                    <TableHead>{t('cart.quantity')}</TableHead>
                    <TableHead>{t('cart.total')}</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {cartItems.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell>
                        <div className="flex items-center space-x-3">
                          {item.product && (
                            <>
                              <div className="relative h-16 w-16 rounded-md overflow-hidden">
                                <Image
                                  src={item.product.imageUrl}
                                  alt={item.product.name}
                                  fill
                                  className="object-cover"
                                />
                              </div>
                              <div>
                                <Link
                                  href={`/products/${item.product.id}`}
                                  className="font-medium hover:text-primary"
                                >
                                  {item.product.name}
                                </Link>
                                <p className="text-sm text-muted-foreground">
                                  {item.product.brand}
                                </p>
                              </div>
                            </>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        {item.product && formatPrice(item.product.price)}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                            disabled={item.quantity <= 1}
                          >
                            <Minus className="h-3 w-3" />
                          </Button>
                          <span className="w-8 text-center">{item.quantity}</span>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          >
                            <Plus className="h-3 w-3" />
                          </Button>
                        </div>
                      </TableCell>
                      <TableCell>
                        {item.product && formatPrice(item.product.price * item.quantity)}
                      </TableCell>
                      <TableCell>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => removeItem(item.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>{t('cart.orderSummary')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>{t('cart.subtotal')}</span>
                  <span>{formatPrice(getTotalPrice())}</span>
                </div>
                <div className="flex justify-between">
                  <span>{t('cart.shipping')}</span>
                  <span>{t('cart.free')}</span>
                </div>
                <div className="flex justify-between">
                  <span>{t('cart.tax')}</span>
                  <span>{formatPrice(getTotalPrice() * 0.08)}</span>
                </div>
              </div>

              <Separator />

              <div className="flex justify-between font-semibold text-lg">
                <span>{t('cart.grandTotal')}</span>
                <span>{formatPrice(getTotalPrice() * 1.08)}</span>
              </div>

              <Button className="w-full" size="lg">
                {t('cart.checkout')}
              </Button>

              <Button variant="outline" className="w-full" asChild>
                <Link href="/products">{t('cart.continueShopping')}</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
