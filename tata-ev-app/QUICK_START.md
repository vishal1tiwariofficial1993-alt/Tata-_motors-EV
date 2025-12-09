# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Navigate to Project
```bash
cd path/to/tata-ev-app/backend
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```

### 5. Open in Browser
```
http://localhost:5000
```

---

## Feature Quick Links

Once the app is running:

| Feature | URL |
|---------|-----|
| **Home** | http://localhost:5000/ |
| **EV Recommender** | http://localhost:5000/templates/recommend.html |
| **Range Simulator** | http://localhost:5000/templates/range.html |
| **Cost Comparison** | http://localhost:5000/templates/compare.html |
| **Charger Finder** | http://localhost:5000/templates/chargers.html |
| **Test Drive Booking** | http://localhost:5000/templates/testdrive.html |
| **AI Chat** | http://localhost:5000/templates/chat.html |

---

## API Testing with cURL

### Get All Models
```bash
curl http://localhost:5000/api/models
```

### Get EV Recommendation
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "daily_km": 60,
    "usage_type": "city",
    "budget": 1500000,
    "charging_access": "public"
  }'
```

### Calculate Range
```bash
curl -X POST http://localhost:5000/api/range \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Nexon EV",
    "ac_usage": true,
    "driving_style": "moderate",
    "city_type": "city",
    "temperature": "normal"
  }'
```

### Compare Costs
```bash
curl -X POST http://localhost:5000/api/compare-cost \
  -H "Content-Type: application/json" \
  -d '{
    "daily_km": 60,
    "fuel_price": 105,
    "electricity_rate": 8,
    "years": 5,
    "ev_price": 1500000,
    "petrol_price": 1000000
  }'
```

### Find Chargers
```bash
curl "http://localhost:5000/api/chargers?city=Mumbai&charger_type=DC"
```

### Chat with AI
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the best EV for city driving?"}'
```

### Book Test Drive
```bash
curl -X POST http://localhost:5000/api/testdrive/book \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "model": "Nexon EV",
    "preferred_date": "2025-12-20",
    "preferred_time": "10:00",
    "city": "Mumbai"
  }'
```

---

## File Structure Explained

```
backend/
├── app.py                          # Main Flask app - all routes and endpoints
├── requirements.txt                # Python packages to install
│
├── modules/                        # Core business logic
│   ├── ai_service.py              # AI/LLM integration (mock + real integration point)
│   ├── ev_models.py               # EV database and recommendation algorithm
│   ├── charging_stations.py       # Charging station database (20+ stations)
│   └── cost_calculator.py         # Cost calculation and comparison logic
│
├── templates/                      # HTML pages (7 pages)
│   ├── index.html                 # Home page with features
│   ├── recommend.html             # AI recommender interface
│   ├── range.html                 # Range simulator
│   ├── compare.html               # Cost comparison tool
│   ├── chargers.html              # Charging station finder
│   ├── testdrive.html             # Test drive booking form
│   └── chat.html                  # AI chat assistant
│
└── static/                         # CSS and JavaScript
    ├── css/style.css              # Complete styling (1000+ lines)
    └── js/main.js                 # Utility functions and API calls
```

---

## Key Features

### ✅ AI Recommender
- Input: Daily km, usage type, budget, charging access
- Output: Best model with alternatives and AI insights
- Algorithm: Multi-factor scoring system

### ✅ Range Simulator
- Input: Model, AC usage, driving style, terrain, temperature
- Output: Real-world range with adjustment factors
- Factors: ±20% variation based on conditions

### ✅ Cost Comparison
- Input: Daily km, fuel price, electricity rate, timeframe
- Output: Monthly/yearly/5-year savings vs petrol
- Includes: Maintenance, insurance, registration costs

### ✅ Charger Finder
- 20+ pre-loaded stations across India
- Filter by: City, charger type, power, cost
- Features: Distance-based search, availability status

### ✅ Test Drive Booking
- Instant form submission
- Booking confirmation with ID
- Ready for email/SMS integration

### ✅ AI Chat
- Natural language responses
- Mock AI responses included
- Integration point for real LLM API

---

## Customization

### Update EV Prices
Edit `modules/ev_models.py` - change `base_price` values

### Add New Models
Add new `EVModel()` instance in `modules/ev_models.py`

### Add Charging Stations
Add new `ChargingStation()` in `modules/charging_stations.py`

### Connect Real LLM
Edit `modules/ai_service.py` - replace mock with OpenAI/Claude/Gemini API

### Change UI Colors
Edit `backend/static/css/style.css` - modify `:root` color variables

---

## Troubleshooting

### Port 5000 in use?
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Module not found error?
```bash
pip install -r requirements.txt
```

### CSS/JS not loading?
Check browser console (F12) for 404 errors. Ensure static files are in correct paths.

---

## Production Deployment

```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress
pip install waitress
waitress-serve --port=5000 app:app
```

---

## Next Steps

1. ✅ App is running locally
2. 📱 Test all features in browser
3. 🔌 Integrate real LLM API (see ai_service.py)
4. 💾 Set up database if needed (SQLAlchemy)
5. 📧 Configure email notifications
6. 🚀 Deploy to production

---

## Support

- Full README: See `README.md`
- API Docs: See README.md → API Documentation
- Issues: Check Flask console output

**Happy Building! 🎉**
