"""
Cost Calculator Module
Calculates EV vs Petrol cost comparisons and savings.
"""

from typing import Dict, Any


class CostCalculator:
    """Calculate and compare EV vs Petrol costs"""
    
    # Default constants (adjustable per region)
    FUEL_EFFICIENCY_KM_PER_LITER = 18  # Average petrol car efficiency
    EV_EFFICIENCY_KM_PER_KWH = 5  # Average EV efficiency
    
    @staticmethod
    def calculate_monthly_cost(daily_km: float, fuel_price: float, 
                              electricity_rate: float, 
                              vehicle_type: str = "petrol") -> Dict[str, Any]:
        """
        Calculate monthly fuel/electricity cost.
        
        Args:
            daily_km: Daily driving distance
            fuel_price: Price per liter (petrol) or per kWh (electricity)
            electricity_rate: Electricity rate in INR per kWh (used for EV)
            vehicle_type: 'petrol' or 'ev'
            
        Returns:
            Dict with cost breakdown
        """
        monthly_km = daily_km * 30
        
        if vehicle_type.lower() == "petrol":
            liters_needed = monthly_km / CostCalculator.FUEL_EFFICIENCY_KM_PER_LITER
            monthly_cost = liters_needed * fuel_price
            return {
                "vehicle_type": "Petrol",
                "monthly_km": monthly_km,
                "monthly_fuel_liters": round(liters_needed, 2),
                "fuel_price": fuel_price,
                "monthly_cost": round(monthly_cost, 2),
                "cost_per_km": round(monthly_cost / monthly_km, 2) if monthly_km > 0 else 0
            }
        
        elif vehicle_type.lower() == "ev":
            kwh_needed = monthly_km / CostCalculator.EV_EFFICIENCY_KM_PER_KWH
            monthly_cost = kwh_needed * electricity_rate
            return {
                "vehicle_type": "EV",
                "monthly_km": monthly_km,
                "monthly_kwh": round(kwh_needed, 2),
                "electricity_rate": electricity_rate,
                "monthly_cost": round(monthly_cost, 2),
                "cost_per_km": round(monthly_cost / monthly_km, 2) if monthly_km > 0 else 0
            }
    
    @staticmethod
    def compare_costs(daily_km: float, fuel_price: float, 
                     electricity_rate: float, years: int = 1) -> Dict[str, Any]:
        """
        Compare EV vs Petrol costs over specified period.
        
        Args:
            daily_km: Daily driving distance
            fuel_price: Petrol price per liter (INR)
            electricity_rate: Electricity rate per kWh (INR)
            years: Number of years for comparison
            
        Returns:
            Dict with detailed cost comparison
        """
        total_km = daily_km * 365 * years
        
        # Petrol cost calculation
        petrol_liters = total_km / CostCalculator.FUEL_EFFICIENCY_KM_PER_LITER
        petrol_cost = petrol_liters * fuel_price
        
        # EV cost calculation (electricity only)
        ev_kwh = total_km / CostCalculator.EV_EFFICIENCY_KM_PER_KWH
        ev_electricity_cost = ev_kwh * electricity_rate
        
        # Additional EV maintenance savings
        ev_maintenance_savings = total_km * 0.5 / 1000  # ₹0.5 per km (conservative)
        ev_total_cost = ev_electricity_cost - ev_maintenance_savings
        
        # Calculate savings
        total_savings = petrol_cost - ev_total_cost
        monthly_savings = total_savings / (years * 12) if years > 0 else 0
        
        return {
            "period_years": years,
            "total_km": total_km,
            "petrol": {
                "liters_required": round(petrol_liters, 2),
                "fuel_cost": round(petrol_cost, 2),
                "maintenance_cost": round(total_km * 2 / 1000, 2),  # ₹2 per km
                "total_cost": round(petrol_cost + (total_km * 2 / 1000), 2)
            },
            "ev": {
                "kwh_required": round(ev_kwh, 2),
                "electricity_cost": round(ev_electricity_cost, 2),
                "maintenance_savings": round(ev_maintenance_savings, 2),
                "total_cost": round(ev_total_cost, 2)
            },
            "savings": {
                "total_savings": round(total_savings, 2),
                "monthly_savings": round(monthly_savings, 2),
                "yearly_savings": round(total_savings / years, 2) if years > 0 else 0,
                "savings_percentage": round((total_savings / petrol_cost * 100), 2) if petrol_cost > 0 else 0
            }
        }
    
    @staticmethod
    def calculate_breakeven(vehicle_price_diff: float, daily_km: float, 
                           fuel_price: float, electricity_rate: float) -> Dict[str, Any]:
        """
        Calculate breakeven point between EV and Petrol.
        
        Args:
            vehicle_price_diff: Price difference (EV - Petrol)
            daily_km: Daily driving distance
            fuel_price: Petrol price per liter
            electricity_rate: Electricity rate per kWh
            
        Returns:
            Dict with breakeven analysis
        """
        # Calculate daily savings
        daily_petrol_cost = (daily_km / CostCalculator.FUEL_EFFICIENCY_KM_PER_LITER) * fuel_price
        daily_ev_cost = (daily_km / CostCalculator.EV_EFFICIENCY_KM_PER_KWH) * electricity_rate
        daily_savings = daily_petrol_cost - daily_ev_cost
        
        if daily_savings <= 0:
            return {
                "breakeven_possible": False,
                "reason": "EV daily cost exceeds petrol cost at given rates"
            }
        
        # Calculate breakeven time
        days_to_breakeven = vehicle_price_diff / daily_savings if daily_savings > 0 else float('inf')
        years_to_breakeven = days_to_breakeven / 365
        
        return {
            "breakeven_possible": True,
            "price_difference": round(vehicle_price_diff, 2),
            "daily_savings": round(daily_savings, 2),
            "days_to_breakeven": round(days_to_breakeven, 2),
            "years_to_breakeven": round(years_to_breakeven, 2),
            "km_to_breakeven": round(days_to_breakeven * daily_km, 2),
            "breakeven_summary": f"You'll save the EV price difference in {years_to_breakeven:.1f} years ({days_to_breakeven:.0f} days) with {daily_km}km daily driving"
        }
    
    @staticmethod
    def get_total_cost_of_ownership(vehicle_price: float, years: int, 
                                   daily_km: float, fuel_price: float, 
                                   electricity_rate: float, 
                                   vehicle_type: str = "petrol") -> Dict[str, Any]:
        """
        Calculate total cost of ownership for specified period.
        
        Args:
            vehicle_price: Vehicle price in INR
            years: Ownership period in years
            daily_km: Daily driving distance
            fuel_price: Fuel price per liter
            electricity_rate: Electricity rate per kWh
            vehicle_type: 'petrol' or 'ev'
            
        Returns:
            Dict with total cost of ownership
        """
        total_km = daily_km * 365 * years
        
        if vehicle_type.lower() == "ev":
            kwh_needed = total_km / CostCalculator.EV_EFFICIENCY_KM_PER_KWH
            fuel_cost = kwh_needed * electricity_rate
            maintenance_cost = total_km * 0.5 / 1000  # ₹0.5 per km
            insurance_cost = 0.03 * vehicle_price * years  # 3% of price per year
        else:
            liters_needed = total_km / CostCalculator.FUEL_EFFICIENCY_KM_PER_LITER
            fuel_cost = liters_needed * fuel_price
            maintenance_cost = total_km * 2 / 1000  # ₹2 per km
            insurance_cost = 0.05 * vehicle_price * years  # 5% of price per year
        
        registration_tax = 0.12 * vehicle_price
        total_tco = vehicle_price + fuel_cost + maintenance_cost + insurance_cost + registration_tax
        cost_per_km = total_tco / total_km if total_km > 0 else 0
        
        return {
            "vehicle_type": vehicle_type.upper(),
            "ownership_years": years,
            "total_km": total_km,
            "vehicle_price": round(vehicle_price, 2),
            "fuel_cost": round(fuel_cost, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "insurance_cost": round(insurance_cost, 2),
            "registration_tax": round(registration_tax, 2),
            "total_tco": round(total_tco, 2),
            "cost_per_km": round(cost_per_km, 2)
        }


# Example usage functions
def compare_tco(ev_price: float, petrol_price: float, years: int, 
                daily_km: float, fuel_price: float, electricity_rate: float) -> Dict[str, Any]:
    """
    Compare total cost of ownership between EV and Petrol.
    """
    ev_tco = CostCalculator.get_total_cost_of_ownership(
        ev_price, years, daily_km, fuel_price, electricity_rate, "ev"
    )
    petrol_tco = CostCalculator.get_total_cost_of_ownership(
        petrol_price, years, daily_km, fuel_price, electricity_rate, "petrol"
    )
    
    return {
        "ev": ev_tco,
        "petrol": petrol_tco,
        "comparison": {
            "ev_cheaper": ev_tco["total_tco"] < petrol_tco["total_tco"],
            "savings": round(petrol_tco["total_tco"] - ev_tco["total_tco"], 2),
            "cost_per_km_difference": round(petrol_tco["cost_per_km"] - ev_tco["cost_per_km"], 2)
        }
    }
