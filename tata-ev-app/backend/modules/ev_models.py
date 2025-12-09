"""
EV Models Database Module
Contains Tata Motors EV models database and recommendation logic.
"""

from typing import Dict, List, Any


class EVModel:
    """Represents a Tata EV model"""
    
    def __init__(self, name: str, base_price: float, range_km: float, 
                 charging_time: Dict[str, float], best_for: List[str]):
        """
        Initialize EV Model
        
        Args:
            name: Model name
            base_price: Starting price in INR
            range_km: Certified range in km
            charging_time: Dict with 'ac_7kw' and 'dc_50kw' times in hours
            best_for: List of ideal use cases
        """
        self.name = name
        self.base_price = base_price
        self.range_km = range_km
        self.charging_time = charging_time
        self.best_for = best_for
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "name": self.name,
            "base_price": self.base_price,
            "range_km": self.range_km,
            "charging_time": self.charging_time,
            "best_for": self.best_for
        }


class EVModelsDatabase:
    """Database of Tata Motors EV models"""
    
    def __init__(self):
        """Initialize with current Tata EV lineup"""
        self.models = {
            "punch_ev": EVModel(
                name="Tata Punch EV",
                base_price=850000,  # ₹8.5L
                range_km=315,
                charging_time={"ac_7kw": 9.5, "dc_50kw": 0.75},
                best_for=["city_commute", "budget_conscious", "daily_driving"]
            ),
            "nexon_ev": EVModel(
                name="Tata Nexon EV",
                base_price=1500000,  # ₹15L
                range_km=440,
                charging_time={"ac_7kw": 12, "dc_50kw": 1},
                best_for=["highway", "comfort", "performance"]
            ),
            "nexon_ev_plus": EVModel(
                name="Tata Nexon EV Plus",
                base_price=1850000,  # ₹18.5L
                range_km=480,
                charging_time={"ac_7kw": 14, "dc_50kw": 1.2},
                best_for=["long_distance", "highway", "premium_comfort"]
            ),
            "tigor_ev": EVModel(
                name="Tata Tigor EV",
                base_price=900000,  # ₹9L
                range_km=360,
                charging_time={"ac_7kw": 8, "dc_50kw": 0.65},
                best_for=["sedan_lovers", "city_driving", "space_conscious"]
            ),
            "harrier_ev": EVModel(
                name="Tata Harrier EV (Upcoming)",
                base_price=2500000,  # ₹25L
                range_km=500,
                charging_time={"ac_7kw": 16, "dc_50kw": 1.3},
                best_for=["luxury_segment", "large_family", "premium_experience"]
            )
        }
    
    def recommend_model(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend best EV model based on user criteria.
        
        Args:
            criteria: Dict with keys:
                - daily_km: Daily driving distance
                - usage_type: 'city', 'highway', or 'mix'
                - budget: Budget in INR
                - charging_access: 'home', 'public', or 'both'
                
        Returns:
            Dict with recommended model and reasoning
        """
        daily_km = criteria.get("daily_km", 50)
        usage_type = criteria.get("usage_type", "city")
        budget = criteria.get("budget", 1500000)
        charging_access = criteria.get("charging_access", "public")
        
        recommendations = []
        
        # Score each model based on criteria
        for model_key, model in self.models.items():
            score = 0
            reasoning = []
            
            # Budget check (40% weight)
            if model.base_price <= budget:
                budget_score = 40
                reasoning.append(f"Within budget (₹{budget/100000:.1f}L)")
            else:
                budget_score = max(0, 40 - (model.base_price - budget) / 50000)
                reasoning.append(f"Slightly above budget, but worth consideration")
            score += budget_score
            
            # Range check (30% weight)
            required_range = daily_km * 1.5  # 1.5x daily km for safety margin
            if model.range_km >= required_range:
                range_score = 30
                reasoning.append(f"Excellent range for {daily_km}km daily driving")
            elif model.range_km >= daily_km:
                range_score = 20
                reasoning.append(f"Adequate range with careful planning")
            else:
                range_score = 10
                reasoning.append(f"May need frequent charging")
            score += range_score
            
            # Usage type match (20% weight)
            if usage_type in model.best_for:
                score += 20
                reasoning.append(f"Perfect for {usage_type} driving")
            elif "city" in model.best_for and usage_type == "city":
                score += 15
            elif "highway" in model.best_for and usage_type == "highway":
                score += 15
            
            # Charging access (10% weight)
            if charging_access == "public" or charging_access == "both":
                score += 10
                reasoning.append("Works well with public charging networks")
            
            recommendations.append({
                "model": model,
                "score": score,
                "reasoning": reasoning
            })
        
        # Sort by score and return top recommendation
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        if recommendations:
            best = recommendations[0]
            return {
                "recommended_model": best["model"].to_dict(),
                "score": best["score"],
                "reasoning": " | ".join(best["reasoning"]),
                "alternatives": [r["model"].to_dict() for r in recommendations[1:3]]
            }
        
        return {"error": "No models found matching criteria"}
    
    def get_all_models(self) -> List[Dict[str, Any]]:
        """Get all available EV models"""
        return [model.to_dict() for model in self.models.values()]
    
    def get_model_by_name(self, name: str) -> Dict[str, Any]:
        """Get specific model by name"""
        for model in self.models.values():
            if name.lower() in model.name.lower():
                return model.to_dict()
        return {"error": f"Model '{name}' not found"}


# Initialize database singleton
ev_db = EVModelsDatabase()
