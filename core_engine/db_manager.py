
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="citycore_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.is_connected = False
        
        # Folder check kar lo taaki CSV backup mein koi dikkat na aaye
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Jaise hi object bane, connection try karo
        self.connect_database()

    def connect_database(self):
        try:
            # MySQL se connection banane ki koshish kar rahe hain
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.is_connected = True
                print("--> Bhai, MySQL Database ke sath connection ekdum successful hai!")
        except Error as e:
            # Agar sir ke PC pe password galat hua ya SQL band hua, toh yahan aayega
            self.is_connected = False
            print(f"--> Oho! MySQL connect nahi ho paya: {e}")
            print("--> Tension mat le, system automatic CSV Fallback Mode par switch ho raha hai.")

    def fetch_zones_data(self):
        # Agar SQL chal raha hai toh wahan se data lao, nahi toh CSV se padh lo bhai
        if self.is_connected:
            try:
                query = "SELECT * FROM city_zones"
                df = pd.read_sql(query, self.connection)
                return df
            except Error as e:
                print(f"--> Query chalane mein dikkat aayi: {e}")
        
        # Fallback: Agar SQL fail hua toh local CSV file check karenge
        csv_path = "data/zone_telemetry.csv"
        if os.path.exists(csv_path):
            print("--> CSV file se data utha rahe hain (Fallback Mode)...")
            return pd.read_csv(csv_path)
        else:
            print("--> Na toh SQL mila aur na hi CSV file mili bhai!")
            return pd.DataFrame()

    def save_log_to_csv(self, df, filename="data/economy_history.csv"):
        # Pandas DataFrame ko seedha CSV mein save karne ka jugaad
        try:
            df.to_csv(filename, index=False)
            print(f"--> Data successfully {filename} mein export ho gaya hai!")
        except Exception as e:
            print(f"--> CSV save karte waqt error aa gaya: {e}")

    def close_connection(self):
        # Kaam khatam hone par connection close karna zaroori hai
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("--> MySQL connection safely band kar diya gaya hai.")

# Test karne ke liye agar directly yeh file run ki jaye
if __name__ == "__main__":
    db = DatabaseManager(password="Yahan_Apna_Password_Dal_Lena")
    df_zones = db.fetch_zones_data()
    print("Fetched Zones Data:\n", df_zones)
    db.close_connection()