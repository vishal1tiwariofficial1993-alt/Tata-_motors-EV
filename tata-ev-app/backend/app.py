"""
Tata Motors EV Web Application
Production-Ready Flask Backend
Author: Design Thinking Team
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
from datetime import datetime
from typing import Dict, Any

# Import custom modules
from modules.ai_service import ai_service
from modules.ev_models import ev_db
from modules.charging_stations import charging_db
from modules.cost_calculator import CostCalculator, compare_tco

# ============================================
# FLASK APP INITIALIZATION
# ============================================

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"
CORS(app)

# In-memory storage for test drives (replace with database in production)
test_drive_bookings = []

# ============================================
# HOME ROUTE
# ============================================

@app.route("/")
def index():
    """
    Home page - Main landing page.
    GET request handler.
    """
    return render_template("index.html")


# ============================================
# PAGE ROUTES (FOR NAVIGATION)
# ============================================

@app.route("/recommend")
def recommend_page():
    """EV Recommender page"""
    return render_template("recommend.html")


@app.route("/range")
def range_page():
    """Range Simulator page"""
    return render_template("range.html")


@app.route("/compare")
def compare_page():
    """Cost Comparison page"""
    return render_template("compare.html")


@app.route("/chargers")
def chargers_page():
    """Charger Finder page"""
    return render_template("chargers.html")


@app.route("/testdrive")
def testdrive_page():
    """Test Drive Booking page"""
    return render_template("testdrive.html")


@app.route("/chat")
def chat_page():
    """AI Chat Assistant page"""
    return render_template("chat.html")


# ============================================
# EV RECOMMENDATION ENDPOINTS
# ============================================

@app.route("/api/recommend", methods=["POST"])
def recommend_ev():
    """
    AI-Powered EV Recommendation Engine.
    
    Expected JSON input:
    {
        "daily_km": 60,
        "usage_type": "city",  # city, highway, or mix
        "budget": 1500000,
        "charging_access": "public"  # home, public, or both
    }
    
    Returns: Recommended model with reasoning and alternatives
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not all(key in data for key in ["daily_km", "usage_type", "budget", "charging_access"]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Get recommendation from database
        recommendation = ev_db.recommend_model({
            "daily_km": data.get("daily_km"),
            "usage_type": data.get("usage_type"),
            "budget": data.get("budget"),
            "charging_access": data.get("charging_access")
        })
        
        # Enhance with AI insights
        ai_insight = ai_service.generate_ai_response(
            f"The user wants to buy an EV with {data.get('daily_km')}km daily driving, "
            f"budget ₹{data.get('budget')/100000:.1f}L, and {data.get('usage_type')} usage. "
            f"Recommend the best Tata EV."
        )
        
        recommendation["ai_insight"] = ai_insight
        
        return jsonify(recommendation)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def get_all_models():
    """
    Get all available Tata EV models.
    
    Returns: List of all models with specifications
    """
    try:
        models = ev_db.get_all_models()
        return jsonify({"models": models})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# RANGE SIMULATOR ENDPOINTS
# ============================================

@app.route("/api/range", methods=["POST"])
def calculate_range():
    """
    Range Simulator with real-world adjustments.
    
    Expected JSON input:
    {
        "model": "Nexon EV",
        "ac_usage": true,
        "driving_style": "moderate",  # aggressive, moderate, eco
        "city_type": "city",  # city, highway, mix
        "temperature": "normal"  # cold, normal, hot
    }
    
    Returns: Adjusted range estimate
    """
    try:
        data = request.get_json()
        
        # Get base model range
        model = ev_db.get_model_by_name(data.get("model"))
        if "error" in model:
            return jsonify(model), 404
        
        base_range = model["range_km"]
        
        # Calculate adjusted range using AI
        conditions = {
            "ac_usage": data.get("ac_usage", False),
            "driving_style": data.get("driving_style", "moderate"),
            "city_type": data.get("city_type", "mix"),
            "temperature": data.get("temperature", "normal")
        }
        
        adjusted_range = ai_service.refine_range_prediction(base_range, conditions)
        
        # Get AI explanation
        ai_explanation = ai_service.generate_ai_response(
            f"A {data.get('model')} with base range {base_range}km will have approximately "
            f"{adjusted_range}km range. Explain why based on {conditions}."
        )
        
        return jsonify({
            "model": data.get("model"),
            "base_range_km": base_range,
            "adjusted_range_km": adjusted_range,
            "adjustment_factors": conditions,
            "explanation": ai_explanation
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# COST COMPARISON ENDPOINTS
# ============================================

@app.route("/api/compare-cost", methods=["POST"])
def compare_costs():
    """
    EV vs Petrol Cost Comparison.
    
    Expected JSON input:
    {
        "daily_km": 60,
        "fuel_price": 105,  # INR per liter
        "electricity_rate": 8,  # INR per kWh
        "years": 5,
        "ev_price": 1500000,
        "petrol_price": 1000000
    }
    
    Returns: Detailed cost comparison and savings
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["daily_km", "fuel_price", "electricity_rate", "years"]
        if not all(key in data for key in required):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Compare costs
        comparison = CostCalculator.compare_costs(
            daily_km=data.get("daily_km"),
            fuel_price=data.get("fuel_price"),
            electricity_rate=data.get("electricity_rate"),
            years=data.get("years")
        )
        
        # Add TCO if vehicle prices provided
        if "ev_price" in data and "petrol_price" in data:
            tco_comparison = compare_tco(
                ev_price=data.get("ev_price"),
                petrol_price=data.get("petrol_price"),
                years=data.get("years"),
                daily_km=data.get("daily_km"),
                fuel_price=data.get("fuel_price"),
                electricity_rate=data.get("electricity_rate")
            )
            comparison["tco"] = tco_comparison
        
        return jsonify(comparison)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# CHARGING STATION FINDER ENDPOINTS
# ============================================

@app.route("/api/chargers", methods=["GET"])
def get_chargers():
    """
    Get all charging stations or filter by criteria.
    
    Query parameters:
    - city: Filter by city name
    - charger_type: AC or DC
    - min_power_kw: Minimum charging power
    - max_cost_per_kwh: Maximum cost per kWh
    
    Returns: List of charging stations matching filters
    """
    try:
        # Build filter criteria from query parameters
        filters = {}
        
        if request.args.get("city"):
            filters["city"] = request.args.get("city")
        
        if request.args.get("charger_type"):
            filters["charger_type"] = request.args.get("charger_type")
        
        if request.args.get("min_power_kw"):
            filters["min_power_kw"] = float(request.args.get("min_power_kw"))
        
        if request.args.get("max_cost_per_kwh"):
            filters["max_cost_per_kwh"] = float(request.args.get("max_cost_per_kwh"))
        
        # Get filtered stations
        if filters:
            stations = charging_db.filter_stations(filters)
        else:
            stations = charging_db.get_all_stations()
        
        return jsonify({"stations": stations, "count": len(stations)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chargers/nearby", methods=["POST"])
def get_nearby_chargers():
    """
    Get charging stations near given coordinates.
    
    Expected JSON input:
    {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "radius_km": 10
    }
    
    Returns: Nearby charging stations sorted by distance
    """
    try:
        data = request.get_json()
        
        stations = charging_db.get_nearby_stations(
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            radius_km=data.get("radius_km", 10)
        )
        
        return jsonify({"stations": stations, "count": len(stations)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chargers/fast", methods=["GET"])
def get_fast_chargers():
    """
    Get only fast DC charging stations.
    
    Returns: List of fast (50kW+) DC chargers
    """
    try:
        stations = charging_db.get_fast_chargers()
        return jsonify({"stations": stations, "count": len(stations)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# TEST DRIVE BOOKING ENDPOINTS
# ============================================

@app.route("/api/testdrive/book", methods=["POST"])
def book_test_drive():
    """
    Submit test drive booking request.
    
    Expected JSON input:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "model": "Nexon EV",
        "preferred_date": "2025-12-20",
        "preferred_time": "10:00",
        "city": "Mumbai"
    }
    
    Returns: Booking confirmation
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ["name", "email", "phone", "model", "preferred_date", "preferred_time", "city"]
        if not all(key in data for key in required):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Create booking record
        booking = {
            "booking_id": f"TD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "model": data.get("model"),
            "preferred_date": data.get("preferred_date"),
            "preferred_time": data.get("preferred_time"),
            "city": data.get("city"),
            "booking_timestamp": datetime.now().isoformat(),
            "status": "Pending"
        }
        
        # Store booking (in production, save to database)
        test_drive_bookings.append(booking)
        
        return jsonify({
            "success": True,
            "message": f"Test drive booked successfully!",
            "booking": booking
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/testdrive/bookings", methods=["GET"])
def get_test_drive_bookings():
    """
    Get all test drive bookings (admin endpoint).
    
    Returns: List of all bookings
    """
    try:
        return jsonify({
            "bookings": test_drive_bookings,
            "total": len(test_drive_bookings)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# AI CHAT ASSISTANT ENDPOINTS
# ============================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    AI Chat Assistant endpoint.
    
    Expected JSON input:
    {
        "message": "What is the best EV for city driving?",
        "conversation_id": "conv-123"  # Optional, for conversation history
    }
    
    Returns: AI-generated response
    """
    try:
        data = request.get_json()
        
        if "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        user_message = data.get("message")
        
        # Get AI response
        ai_response = ai_service.chat_assistant(user_message)
        
        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔋 Tata Motors EV Web Application")
    print("Starting Flask Development Server...")
    print("=" * 60)
    print("📍 Server: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/")
    print("=" * 60)
    
    # Run development server on port 8000
    app.run(debug=True, host="0.0.0.0", port=8000)
