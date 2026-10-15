import time
import pandas as pd

# Apne banaye hue sare custom modules import kar rahe hain
from core_engine.db_manager import DatabaseManager
from core_engine.map_fetcher import MapFetcher
from core_engine.world_builder_3d import CityWorld3D
from core_engine.economy_simulation import EconomySimulation
from core_engine.traffic_router import TrafficRouter
from core_engine.ml_predictor import AIPredictiveAnalyzer
from core_engine.live_analytics import LiveAnalytics

def main():
    print("==================================================")
    print("      CITYCORE-3D: Smart City Engine Starting...  ")
    print("==================================================")

    # 1. Database Manager Initialize karo (SQL / CSV Fallback ke sath)
    db = DatabaseManager()

    # 2. Map Fetcher se Asli Data lao (Jaise 'Roorkee' ya 'Mumbai')
    city_name = "Roorkee"
    fetcher = MapFetcher()
    df_buildings = fetcher.fetch_real_world_data(city_name)

    # 3. Economy Simulation aur AI Predictor shuru karo
    economy = EconomySimulation(initial_budget=15000000.0, initial_population=30000)
    ai_analyzer = AIPredictiveAnalyzer()
    traffic = TrafficRouter()
    traffic.setup_city_intersections()

    # Ek simulation tick run karke dekhte hain ki sab theek chal raha hai ya nahi
    active_count = len(df_buildings)
    tick_result = economy.run_simulation_tick(active_count)
    print(f"--> Initial Tick Telemetry: {tick_result}")

    # 4. 3D Ursina World Builder launch karo aur buildings render karo
    print("--> 3D Ursina Engine launch ho raha hai. WASD se ghoomein aur 'B' dabakar Blueprint Mode dekhein!")
    world = CityWorld3D()
    world.build_city_grid(df_buildings)

    # 5. Live Analytics graph trigger karne ke liye background data save kar do
    history_df = pd.DataFrame([tick_result])
    db.save_log_to_csv(history_df, filename="data/economy_history.csv")

    # 6. Game loop run kar do
    try:
        world.run()
    except KeyboardInterrupt:
        print("\n--> Simulation ko safely band kiya ja raha hai...")
    finally:
        db.close_connection()
        print("--> CityCore-3D successfully closed. Thanks for exploring!")

if __name__ == "__main__":
    main()