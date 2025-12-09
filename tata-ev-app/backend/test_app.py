"""
Tata Motors EV Platform - Test Suite
Unit and integration tests for backend functionality
Run with: pytest
"""

import pytest
import json
from app import app
from modules.ev_models import ev_db
from modules.cost_calculator import CostCalculator
from modules.charging_stations import charging_db


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ========================================
# HOME PAGE TESTS
# ========================================

def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tata Motors EV' in response.data


# ========================================
# EV MODELS TESTS
# ========================================

def test_get_all_models(client):
    """Test getting all EV models"""
    response = client.get('/api/models')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'models' in data
    assert len(data['models']) >= 5
    assert data['models'][0]['name']


def test_recommendation_basic(client):
    """Test basic EV recommendation"""
    criteria = {
        "daily_km": 60,
        "usage_type": "city",
        "budget": 1500000,
        "charging_access": "public"
    }
    response = client.post('/api/recommend', 
                          json=criteria,
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'recommended_model' in data
    assert data['recommended_model']['name']


def test_recommendation_high_budget(client):
    """Test recommendation with high budget"""
    criteria = {
        "daily_km": 200,
        "usage_type": "highway",
        "budget": 3000000,
        "charging_access": "both"
    }
    response = client.post('/api/recommend', json=criteria)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['recommended_model']['base_price'] <= 3000000


def test_recommendation_missing_fields(client):
    """Test recommendation with missing fields"""
    criteria = {
        "daily_km": 60,
        "budget": 1500000
        # Missing usage_type and charging_access
    }
    response = client.post('/api/recommend', json=criteria)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


# ========================================
# RANGE CALCULATION TESTS
# ========================================

def test_range_calculation(client):
    """Test range calculation"""
    data = {
        "model": "Nexon EV",
        "ac_usage": False,
        "driving_style": "eco",
        "city_type": "highway",
        "temperature": "normal"
    }
    response = client.post('/api/range', json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['base_range_km'] > 0
    assert result['adjusted_range_km'] > 0


def test_range_with_ac(client):
    """Test that AC reduces range"""
    data_without_ac = {
        "model": "Punch EV",
        "ac_usage": False,
        "driving_style": "moderate",
        "city_type": "mix",
        "temperature": "normal"
    }
    data_with_ac = data_without_ac.copy()
    data_with_ac["ac_usage"] = True
    
    resp1 = client.post('/api/range', json=data_without_ac)
    resp2 = client.post('/api/range', json=data_with_ac)
    
    range1 = json.loads(resp1.data)['adjusted_range_km']
    range2 = json.loads(resp2.data)['adjusted_range_km']
    
    assert range1 > range2  # AC reduces range


# ========================================
# COST COMPARISON TESTS
# ========================================

def test_cost_comparison(client):
    """Test cost comparison"""
    data = {
        "daily_km": 60,
        "fuel_price": 105,
        "electricity_rate": 8,
        "years": 5,
        "ev_price": 1500000,
        "petrol_price": 1000000
    }
    response = client.post('/api/compare-cost', json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'savings' in result
    assert result['savings']['total_savings'] > 0


def test_cost_calculator_petrol(client):
    """Test petrol cost calculation"""
    result = CostCalculator.calculate_monthly_cost(
        daily_km=60,
        fuel_price=105,
        electricity_rate=8,
        vehicle_type="petrol"
    )
    assert result['vehicle_type'] == 'Petrol'
    assert result['monthly_cost'] > 0
    assert result['cost_per_km'] > 0


def test_cost_calculator_ev(client):
    """Test EV cost calculation"""
    result = CostCalculator.calculate_monthly_cost(
        daily_km=60,
        fuel_price=105,
        electricity_rate=8,
        vehicle_type="ev"
    )
    assert result['vehicle_type'] == 'EV'
    assert result['monthly_cost'] > 0
    assert result['cost_per_km'] > 0


def test_ev_cheaper_than_petrol(client):
    """Test that EV is cheaper in total cost"""
    result = CostCalculator.compare_costs(
        daily_km=60,
        fuel_price=105,
        electricity_rate=8,
        years=5
    )
    assert result['savings']['total_savings'] > 0
    assert result['savings']['savings_percentage'] > 0


# ========================================
# CHARGING STATIONS TESTS
# ========================================

def test_get_all_chargers(client):
    """Test getting all charging stations"""
    response = client.get('/api/chargers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'stations' in data
    assert data['count'] > 0


def test_filter_chargers_by_city(client):
    """Test filtering chargers by city"""
    response = client.get('/api/chargers?city=Mumbai')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(s['city'] == 'Mumbai' for s in data['stations'])


def test_filter_chargers_by_type(client):
    """Test filtering chargers by type"""
    response = client.get('/api/chargers?charger_type=DC')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(s['charger_type'] == 'DC' for s in data['stations'])


def test_fast_chargers(client):
    """Test getting fast chargers only"""
    response = client.get('/api/chargers/fast')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(s['charger_type'] == 'DC' for s in data['stations'])
    assert all(s['power_kw'] >= 50 for s in data['stations'])


def test_nearby_chargers(client):
    """Test finding nearby chargers"""
    data = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "radius_km": 15
    }
    response = client.post('/api/chargers/nearby', json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'stations' in result


# ========================================
# TEST DRIVE BOOKING TESTS
# ========================================

def test_book_test_drive(client):
    """Test booking a test drive"""
    booking_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "model": "Nexon EV",
        "preferred_date": "2025-12-20",
        "preferred_time": "10:00",
        "city": "Mumbai"
    }
    response = client.post('/api/testdrive/book', json=booking_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'booking' in data
    assert data['booking']['booking_id']


def test_book_test_drive_missing_fields(client):
    """Test booking with missing fields"""
    booking_data = {
        "name": "John Doe",
        "email": "john@example.com"
        # Missing required fields
    }
    response = client.post('/api/testdrive/book', json=booking_data)
    assert response.status_code == 400


def test_get_test_drive_bookings(client):
    """Test getting all bookings"""
    response = client.get('/api/testdrive/bookings')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'bookings' in data
    assert 'total' in data


# ========================================
# CHAT ASSISTANT TESTS
# ========================================

def test_chat_basic(client):
    """Test chat assistant"""
    message = {
        "message": "What is the best Tata EV?"
    }
    response = client.post('/api/chat', json=message)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'ai_response' in data
    assert len(data['ai_response']) > 0


def test_chat_range_question(client):
    """Test chat with range question"""
    message = {
        "message": "What is the range of Nexon EV?"
    }
    response = client.post('/api/chat', json=message)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'ai_response' in data


def test_chat_missing_message(client):
    """Test chat with missing message"""
    response = client.post('/api/chat', json={})
    assert response.status_code == 400


# ========================================
# BACKEND LOGIC TESTS
# ========================================

def test_ev_model_database():
    """Test EV model database"""
    models = ev_db.get_all_models()
    assert len(models) >= 5
    assert any(m['name'] == 'Tata Punch EV' for m in models)
    assert any(m['name'] == 'Tata Nexon EV' for m in models)


def test_ev_recommendation_scoring():
    """Test recommendation algorithm"""
    criteria = {
        "daily_km": 100,
        "usage_type": "highway",
        "budget": 1800000,
        "charging_access": "both"
    }
    result = ev_db.recommend_model(criteria)
    assert 'recommended_model' in result
    assert result['score'] > 0


def test_charging_stations_database():
    """Test charging station database"""
    stations = charging_db.get_all_stations()
    assert len(stations) >= 20
    
    # Check data integrity
    for station in stations:
        assert station['name']
        assert station['city']
        assert station['charger_type'] in ['AC', 'DC']
        assert station['power_kw'] > 0


def test_charging_filter():
    """Test charging station filtering"""
    filters = {
        'city': 'Mumbai',
        'charger_type': 'DC',
        'min_power_kw': 50
    }
    stations = charging_db.filter_stations(filters)
    assert all(s['city'] == 'Mumbai' for s in stations)
    assert all(s['charger_type'] == 'DC' for s in stations)
    assert all(s['power_kw'] >= 50 for s in stations)


# ========================================
# ERROR HANDLING TESTS
# ========================================

def test_404_endpoint(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404


def test_invalid_json(client):
    """Test invalid JSON handling"""
    response = client.post('/api/recommend',
                          data='invalid json',
                          content_type='application/json')
    assert response.status_code >= 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
