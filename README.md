# Farm Fresh: AI-Powered Farm-to-Table E-commerce Platform

A full-stack e-commerce platform for farm-fresh products featuring an intelligent AI shopping assistant, seasonal product discovery, and a modern React/Next.js frontend. **Connect directly with local farms and enjoy the freshest organic produce delivered to your table.**

![alt text](.github/res/image-1.png)
![alt text](.github/res/image.png)

## Features

### **Farm-to-Table Experience**

- Direct connection to local farms and producers
- Fresh harvest tracking with harvest dates and farm locations
- Organic certification badges and farming practice transparency
- Seasonal product calendar showing what's fresh each month

### **AI Shopping Assistant**

- Natural language product search and recommendations
- State-of-the-art AI with 1M token context window
- Advanced conversation memory and tool orchestration
- AI-driven product suggestions based on seasonal availability

### **Advanced Search & Discovery**

- Vector-based product discovery using Pinecone
- Filter by organic certification, farm location, and seasonality
- Price range, farm/brand, category, ratings, and availability
- Freshness indicators showing harvest recency

### **Complete E-commerce Experience**

- Persistent cart with real-time updates
- Favorites, likes, and personalized settings
- Real-time stock management and availability
- Farm profiles with stories, practices, and certifications

## Farm-Specific Features

### **Product Information**

- **Harvest Date**: Know exactly when your food was picked
- **Farm Location**: See where your food was grown
- **Organic Certification**: Verified organic products clearly marked
- **Seasonal Availability**: Understand what's in season
- **Unit Types**: Proper pricing per pound, dozen, bunch, etc.

### **Farm Profiles**

- Detailed farm information and stories
- Farming practices and certifications
- Location and contact information
- All products from each farm

### **Seasonal Calendar**

- Interactive calendar showing what's in season
- Peak freshness indicators
- Month-by-month harvest guides
- Seasonal recipe suggestions

## Architecture

```
├── Frontend (Next.js)
│   ├── Modern UI with farm-themed design
│   ├── Responsive design & animations
│   ├── Real-time chat interface
│   ├── Shopping cart & product pages
│   └── Farm-specific components (FarmCard, SeasonalBadge, etc.)
│
├── Backend API (Flask + Python)
│   ├── RESTful API endpoints
│   ├── JWT authentication
│   ├── Farm and product models with farm-specific fields
│   ├── Farm routes for profiles and locations
│   └── AI chatbot integration
│
├── AI Services
│   ├── Google Gemini Flash 2.0
│   ├── LangChain orchestration
│   ├── Pinecone vector database
│   └── Sentence Transformers
│
└── Data Layer
    ├── SQLite database (for dev)
    ├── Farm and product tables with farm-specific fields
    ├── Vector embeddings
    └── Session management
```

## Quick Start

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.12+ (for backend)
- **Google AI Studio** API key
- **Pinecone** account and API key

### Tech

- **Language Model**: Google Gemini Flash 2.0
- **Framework**: LangChain for orchestration
- **Vector Database**: Pinecone for semantic search
- **Embeddings**: Sentence Transformers

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/farm-fresh.git
cd farm-fresh
```

2. Set up the backend:
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

3. Set up the frontend:
```bash
cd apps/web
npm install
cp .env.example .env
```

4. Run the application:
```bash
# Terminal 1 - Backend
cd server
python run.py

# Terminal 2 - Frontend
cd apps/web
npm run dev
```

### Development Guidelines

- Follow TypeScript/Python best practices
- Add tests for new features
- Update documentation
- Ensure code passes linting
- Use earthy, farm-themed colors (greens, browns)
- Prioritize freshness and local sourcing messaging

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products/` - Create product (admin)

### Farms
- `GET /api/farms/` - List all farms
- `GET /api/farms/<id>` - Get farm details with products
- `GET /api/farms/<id>/products` - Get all products from a farm
- `POST /api/farms/` - Create farm (admin)
- `PUT /api/farms/<id>` - Update farm (admin)
- `DELETE /api/farms/<id>` - Delete farm (admin)

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.