
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

class LiveAnalytics:
    def __init__(self, data_path="data/economy_history.csv"):
        self.data_path = data_path
        print("--> Live Analytics & Graph Engine ready ho gaya hai!")

    def load_telemetry_data(self):
        # CSV se economy logs uthane ka jugaad
        if os.path.exists(self.data_path):
            df = pd.read_csv(self.data_path)
            return df
        else:
            # Agar file na mile toh dummy dataframe return kar do taaki graph fat na jaye
            print("--> Telemetry CSV nahi mili, sample data load kar rahe hain...")
            return pd.DataFrame({
                'timestamp': ['2026-10-15 10:00', '2026-10-15 11:00', '2026-10-15 12:00', '2026-10-15 13:00'],
                'current_budget': [10000000.0, 10500000.0, 10200000.0, 11000000.0],
                'happiness_index': [85.0, 88.0, 82.0, 92.0],
                'power_usage_kw': [1200.0, 1350.0, 1100.0, 1500.0]
            })

    def plot_curved_bar_analytics(self):
        df = self.load_telemetry_data()
        
        if df.empty:
            print("--> Graph banane ke liye data hi nahi hai bhai!")
            return

        # Pandas se kuch basic stats nikal lete hain (Teacher ke saamne show-off ke liye!)
        print("--- [PANDAS DATA SUMMARY] ---")
        print(df.describe())
        print("-----------------------------\n")

        # Matplotlib figure setup kar rahe hain
        fig, ax = plt.subplots(figsize=(9, 5), facecolor='#1e1e2f')
        ax.set_facecolor('#2d2d44')

        # X aur Y values set karo
        timestamps = [t.split()[-1] if isinstance(t, str) else str(t) for t in df['timestamp']]
        budgets = df['current_budget'] / 100000.0  # Lakhs mein convert kar diya scaling ke liye

        # Bar width aur positions
        x_pos = range(len(timestamps))
        bar_width = 0.5

        # --- SPECIAL JUGAD: Curved / Rounded Corners Bars using FancyBboxPatch ---
        # Standard blocky bars ki jagah hum stylish curved bars banayenge!
        bars = []
        for i, val in zip(x_pos, budgets):
            # FancyBboxPatch se bars ke upar wale corners rounded ho jayenge
            box = FancyBboxPatch(
                (i - bar_width / 2, 0), 
                bar_width, 
                val,
                boxstyle="round,pad=0.2,rounding_size=0.3",
                facecolor='#00b4d8', 
                edgecolor='#90e0ef',
                linewidth=1.5
            )
            ax.add_patch(box)
            bars.append(box)

        # Axis limits set karo
        ax.set_xlim(-1, len(timestamps))
        ax.set_ylim(0, max(budgets) * 1.2 if not budgets.empty else 10)

        # Graph ki styling aur titles
        ax.set_title("CITYCORE-3D: Live Municipal Budget Analytics", fontsize=14, color='white', fontweight='bold', pad=15)
        ax.set_xlabel("Simulation Time Ticks", fontsize=11, color='#adb5bd')
        ax.set_ylabel("Budget (in Lakhs INR)", fontsize=11, color='#adb5bd')

        # Tick colors aur grid lines white/gray tone mein
        ax.set_xticks(list(x_pos))
        ax.set_xticklabels(timestamps, color='white')
        ax.tick_params(colors='white', which='both')
        ax.grid(True, linestyle='--', alpha=0.2, color='white')

        # Border lines (spines) ko soft kar do
        for spine in ax.spines.values():
            spine.set_color('#495057')

        # Layout adjust karke window khol do
        plt.tight_layout()
        print("--> Matplotlib ka sleek curved bar graph render ho gaya hai!")
        plt.show()

# Test karne ke liye direct run karein
if __name__ == "__main__":
    analytics = LiveAnalytics()
    analytics.plot_curved_bar_analytics()