export interface User {
  id: string;
  email: string;
  name: string;
  preferences: UserPreferences;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface UserPreferences {
  favoriteCategories: string[];
  priceRange: [number, number];
  favoriteBrands: string[];
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  originalPrice?: number;
  category: string;
  subcategory: string;
  brand: string;
  rating: number;
  reviewCount: number;
  imageUrl: string;
  stock: number;
  features: string[];
  isOnSale: boolean;
  salePercentage?: number;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
  inStock: boolean;
  // Farm-specific fields
  harvestDate?: string;
  farmLocation?: string;
  isSeasonal?: boolean;
  organicCertified?: boolean;
  unitType?: string;
  season?: string;
}

export interface Farm {
  id: string;
  name: string;
  description?: string;
  location: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  phone?: string;
  email?: string;
  website?: string;
  imageUrl?: string;
  gallery: string[];
  story?: string;
  practices: string[];
  certifications: string[];
  establishedYear?: number;
  acreage?: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  products?: Product[];
}

export interface ChatMessage {
  id: string;
  chatSessionId: string;
  content: string;
  isBot: boolean;
  type: "text" | "product";
  products?: Product[];
  extraData?: any;
  timestamp: string;
  productDetails?: Product[];
}

export interface ChatSession {
  id: string;
  userId?: string;
  sessionData: any;
  messageCount: number;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
  messages?: ChatMessage[];
}

export interface CartItem {
  id: string;
  user_id: string;
  product_id: string;
  quantity: number;
  created_at: string;
  updated_at: string;
  product?: Product;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  user?: User;
  access_token?: string;
  refresh_token?: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

export interface ProductFilters {
  category?: string;
  subcategory?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  min_rating?: number;
  in_stock_only?: boolean;
  search?: string;
  limit?: number;
}

export interface ProductStats {
  total_products: number;
  total_categories: number;
  total_brands: number;
  price_range: {
    min: number;
    max: number;
  };
  average_rating: number;
  in_stock_count: number;
}
