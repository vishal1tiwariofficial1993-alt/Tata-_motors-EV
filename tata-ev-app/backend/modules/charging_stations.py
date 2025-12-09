"""
Charging Stations Module
Mock dataset of EV charging stations across India.
In production, integrate with real APIs (NITI Aayog, Tata Power, etc.)
"""

from typing import List, Dict, Any


class ChargingStation:
    """Represents an EV charging station"""
    
    def __init__(self, station_id: str, name: str, location: str, 
                 city: str, charger_type: str, power_kw: float, 
                 cost_per_kwh: float, latitude: float, longitude: float):
        """
        Initialize charging station
        
        Args:
            station_id: Unique identifier
            name: Station name
            location: Address/location name
            city: City name
            charger_type: 'AC' or 'DC'
            power_kw: Charging power in kW
            cost_per_kwh: Cost in INR per kWh
            latitude, longitude: GPS coordinates
        """
        self.station_id = station_id
        self.name = name
        self.location = location
        self.city = city
        self.charger_type = charger_type
        self.power_kw = power_kw
        self.cost_per_kwh = cost_per_kwh
        self.latitude = latitude
        self.longitude = longitude
        self.availability = "Available"  # Mock availability
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "station_id": self.station_id,
            "name": self.name,
            "location": self.location,
            "city": self.city,
            "charger_type": self.charger_type,
            "power_kw": self.power_kw,
            "cost_per_kwh": self.cost_per_kwh,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "availability": self.availability,
            "charging_speed": self._get_speed_category()
        }
    
    def _get_speed_category(self) -> str:
        """Categorize charging speed"""
        if self.power_kw < 10:
            return "Slow"
        elif self.power_kw < 50:
            return "Fast"
        else:
            return "Ultra-Fast"


class ChargingStationsDatabase:
    """Database of EV charging stations"""
    
    def __init__(self):
        """Initialize with mock charging station data"""
        self.stations = [
            # Mumbai
            ChargingStation("MH001", "Tata Power Charging Hub", "Worli, Mumbai", "Mumbai", "DC", 50, 8, 19.0176, 72.8194),
            ChargingStation("MH002", "Nexon Care Center", "Vile Parle, Mumbai", "Mumbai", "AC", 7, 10, 19.1136, 72.8481),
            ChargingStation("MH003", "EV Fast Charge", "Andheri, Mumbai", "Mumbai", "DC", 50, 8.5, 19.1136, 72.8697),
            ChargingStation("MH004", "Green Hub Station", "Thane, Mumbai", "Mumbai", "AC", 7, 9.5, 19.2183, 72.9781),
            
            # Delhi
            ChargingStation("DL001", "Delhi EV Hub", "Connaught Place, Delhi", "Delhi", "DC", 50, 7.5, 28.6328, 77.2197),
            ChargingStation("DL002", "Power Station Alpha", "Gurgaon, Delhi", "Delhi", "DC", 50, 8, 28.4595, 77.0266),
            ChargingStation("DL003", "EV Home Charger", "Noida, Delhi", "Delhi", "AC", 7, 9, 28.5921, 77.3869),
            ChargingStation("DL004", "Fast Charge Network", "Dwarka, Delhi", "Delhi", "DC", 50, 8, 28.5355, 77.0411),
            
            # Bangalore
            ChargingStation("KA001", "Nexon Energy Hub", "Whitefield, Bangalore", "Bangalore", "DC", 50, 7, 13.0827, 77.6208),
            ChargingStation("KA002", "Punching Point", "Indiranagar, Bangalore", "Bangalore", "AC", 7, 9, 13.0344, 77.6245),
            ChargingStation("KA003", "Ultra Charge Station", "Koramangala, Bangalore", "Bangalore", "DC", 50, 7.5, 12.9352, 77.6245),
            ChargingStation("KA004", "Eco Charging Zone", "Marathahalli, Bangalore", "Bangalore", "AC", 7, 8.5, 13.0211, 77.6997),
            
            # Pune
            ChargingStation("MH005", "Tata Charging Point", "Hinjewadi, Pune", "Pune", "DC", 50, 7, 18.5912, 73.7499),
            ChargingStation("MH006", "Smart Charge Hub", "Baner, Pune", "Pune", "AC", 7, 9, 18.5596, 73.8140),
            ChargingStation("MH007", "Quick Charge Corner", "Viman Nagar, Pune", "Pune", "DC", 50, 7.5, 18.5672, 73.9108),
            
            # Hyderabad
            ChargingStation("TG001", "Hyderabad EV Hub", "Hitech City, Hyderabad", "Hyderabad", "DC", 50, 7, 17.3850, 78.4867),
            ChargingStation("TG002", "Power Nexus", "Uppal, Hyderabad", "Hyderabad", "AC", 7, 9, 17.3915, 78.5145),
            ChargingStation("TG003", "Charge Station Pro", "Gachibowli, Hyderabad", "Hyderabad", "DC", 50, 7.5, 17.4404, 78.4489),
            
            # Ahmedabad
            ChargingStation("GJ001", "Ahmedabad Charging Network", "Iscon, Ahmedabad", "Ahmedabad", "AC", 7, 8.5, 23.0225, 72.5714),
            ChargingStation("GJ002", "Fast Charge Zone", "Satellite, Ahmedabad", "Ahmedabad", "DC", 50, 7.5, 23.1815, 72.6369),
            
            # Chennai
            ChargingStation("TN001", "Chennai EV Hub", "T. Nagar, Chennai", "Chennai", "AC", 7, 9, 13.0411, 80.2383),
            ChargingStation("TN002", "Quick Charge", "Anna Nagar, Chennai", "Chennai", "DC", 50, 7.5, 13.0856, 80.2103),
        ]
    
    def get_all_stations(self) -> List[Dict[str, Any]]:
        """Get all charging stations"""
        return [station.to_dict() for station in self.stations]
    
    def get_stations_by_city(self, city: str) -> List[Dict[str, Any]]:
        """Get charging stations in a specific city"""
        matching = [s for s in self.stations if s.city.lower() == city.lower()]
        return [station.to_dict() for station in matching]
    
    def get_fast_chargers(self) -> List[Dict[str, Any]]:
        """Get only fast DC chargers (50kW+)"""
        fast = [s for s in self.stations if s.charger_type == "DC" and s.power_kw >= 50]
        return [station.to_dict() for station in fast]
    
    def get_nearby_stations(self, latitude: float, longitude: float, 
                           radius_km: float = 10) -> List[Dict[str, Any]]:
        """
        Get stations within radius of given coordinates.
        Uses simple distance calculation (Haversine approximation).
        """
        nearby = []
        
        for station in self.stations:
            # Simple distance calculation (rough approximation)
            lat_diff = abs(station.latitude - latitude)
            lon_diff = abs(station.longitude - longitude)
            distance = ((lat_diff**2 + lon_diff**2) ** 0.5) * 111  # Approx km per degree
            
            if distance <= radius_km:
                station_dict = station.to_dict()
                station_dict["distance_km"] = round(distance, 2)
                nearby.append(station_dict)
        
        return sorted(nearby, key=lambda x: x["distance_km"])
    
    def filter_stations(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter stations by multiple criteria.
        
        Args:
            filters: Dict with optional keys:
                - city: Filter by city name
                - charger_type: 'AC' or 'DC'
                - min_power_kw: Minimum charging power
                - max_cost_per_kwh: Maximum cost per kWh
        """
        results = self.stations.copy()
        
        # Apply filters
        if "city" in filters and filters["city"]:
            results = [s for s in results if s.city.lower() == filters["city"].lower()]
        
        if "charger_type" in filters and filters["charger_type"]:
            results = [s for s in results if s.charger_type == filters["charger_type"].upper()]
        
        if "min_power_kw" in filters:
            results = [s for s in results if s.power_kw >= filters["min_power_kw"]]
        
        if "max_cost_per_kwh" in filters:
            results = [s for s in results if s.cost_per_kwh <= filters["max_cost_per_kwh"]]
        
        return [station.to_dict() for station in results]


# Initialize database singleton
charging_db = ChargingStationsDatabase()
