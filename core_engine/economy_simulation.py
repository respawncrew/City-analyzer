
import numpy as np
import pandas as pd
from datetime import datetime

class EconomySimulation:
    def __init__(self, initial_budget=10000000.0, initial_population=25000):
        # Shuruat ka budget aur population set kar rahe hain
        self.current_budget = float(initial_budget)
        self.population = int(initial_population)
        self.happiness_index = 100.0  # Public happiness percentage
        self.power_usage_kw = 0.0
        
        # NumPy arrays ka use karke economic coefficients set kar rahe hain (Tech Flex for IP!)
        # [Tax Rate Multiplier, Power Cost per capita, Maintenance Drain]
        self.eco_coefficients = np.array([0.15, 1.2, 5000.0])
        
        print("--> Economy Simulation Engine successfully initialize ho gaya hai!")

    def run_simulation_tick(self, active_buildings_count):
        # Ek simulation tick mein economy update hogi
        
        # 1. NumPy random fluctuation add karenge taaki real-world market jaisa feel aaye
        market_trend = np.random.normal(1.0, 0.05) # Mean 1.0, standard deviation 5%
        
        # 2. Tax collection calculation using population & NumPy array multi
        tax_revenue = self.population * self.eco_coefficients[0] * 10 * market_trend
        
        # 3. Power grid consumption and maintenance cost
        power_drain = active_buildings_count * self.eco_coefficients[1] * 15
        maintenance_cost = active_buildings_count * self.eco_coefficients[2]
        
        # 4. Net budget calculation
        net_cashflow = tax_revenue - maintenance_cost
        self.current_budget += net_cashflow
        self.power_usage_kw = power_drain
        
        # 5. Happiness index adjustments based on budget health
        if self.current_budget < 0:
            self.happiness_index = max(10.0, self.happiness_index - 5.0)
            event_status = "CRITICAL: Municipal Bankruptcy Risk!"
        elif net_cashflow < 0:
            self.happiness_index = max(30.0, self.happiness_index - 1.0)
            event_status = "Warning: Budget deficit detected."
        else:
            self.happiness_index = min(100.0, self.happiness_index + 0.5)
            event_status = "Normal Operations & Economic Growth"

        # Log dictionary return karo taaki database ya CSV mein save ho sake
        tick_log = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'current_budget': round(self.current_budget, 2),
            'happiness_index': round(self.happiness_index, 2),
            'power_usage_kw': round(self.power_usage_kw, 2),
            'active_events': event_status
        }
        
        return tick_log

    def simulate_mass_event(self, event_type="Festival"):
        # Agar shehar mein koi achanak event ho jaye (jaise festival ya power crisis)
        if event_type == "Festival":
            self.current_budget += 500000.0
            self.happiness_index = min(100.0, self.happiness_index + 15.0)
            print("--> Shehar mein Mahaotsav/Festival manaya gaya! Public happiness spike ho gayi.")
        elif event_type == "Blackout":
            self.current_budget -= 200000.0
            self.happiness_index = max(10.0, self.happiness_index - 20.0)
            print("--> Oh no! Power blackout ki wajah se budget aur happiness down ho gayi.")

# Test karne ke liye direct run karein
if __name__ == "__main__":
    sim = EconomySimulation()
    for i in range(3):
        log = sim.run_simulation_tick(active_buildings_count=12)
        print(f"Tick {i+1} Log:", log)