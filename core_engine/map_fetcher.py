import requests
import pandas as pd

class MapFetcher:
    def __init__(self):
        # Overpass API ka public free endpoint
        self.overpass_url = "https://overpass-api.de/api/interpreter"

    def fetch_real_world_data(self, city_name="Roorkee"):
        print(f"--> '{city_name}' ka real-world map data Overpass API se nikal rahe hain...")
        
        # Overpass QL query jo us city ke andar shops, hospitals aur nodes dhoondhegi
        query = f"""
        [out:json][timeout:25];
        area["name"="{city_name}"]->.searchArea;
        (
          node["shop"](area.searchArea);
          node["amenity"~"hospital|school|bank|restaurant"](area.searchArea);
          way["highway"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
        """

        try:
            response = requests.get(self.overpass_url, params={'data': query})
            
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                print(f"--> Wah bhai! Total {len(elements)} elements mil gaye hain {city_name} ke liye.")
                
                parsed_buildings = []
                for el in elements:
                    # Sirf un elements ko lenge jinke paas naam hai
                    if 'tags' in el and 'name' in el['tags']:
                        name = el['tags']['name']
                        b_type = el['tags'].get('shop', el['tags'].get('amenity', 'Landmark'))
                        lat = el.get('lat', 29.8543) # Agar lat na mile toh default de do
                        lon = el.get('lon', 77.8880)
                        
                        # Free image placeholder generator (Bina kisi paid API ke badhiya PNG/Image link)
                        image_link = f"https://via.placeholder.com/300x200.png?text={name.replace(' ', '+')}"
                        
                        parsed_buildings.append({
                            'building_name': name,
                            'building_type': str(b_type).capitalize(),
                            'latitude': lat,
                            'longitude': lon,
                            'image_url': image_link
                        })
                
                # Agar elements mil gaye toh DataFrame mein badal ke return kardo
                if parsed_buildings:
                    df_shops = pd.DataFrame(parsed_buildings)
                    return df_shops
                else:
                    print("--> Is area ke tags mein naam nahi mile, default data use kar rahe hain.")
                    return self.get_fallback_data(city_name)
            else:
                print(f"--> API request fail ho gayi bhai. Status code: {response.status_code}")
                return self.get_fallback_data(city_name)
                
        except Exception as e:
            print(f"--> Error aa gaya map fetch karte waqt: {e}")
            return self.get_fallback_data(city_name)

    def get_fallback_data(self, city_name):
        # Agar internet ya API mein koi dikkat aaye toh local fallback data dega taaki game crash na ho
        print(f"--> Fallback mode active: {city_name} ke liye dummy real data load ho raha hai.")
        fallback_data = [
            {'building_name': f"{city_name} Civil Lines Chowk", 'building_type': 'Landmark', 'latitude': 29.85, 'longitude': 77.88, 'image_url': 'https://via.placeholder.com/300x200.png?text=Civil+Lines'},
            {'building_name': f"{city_name} City Hospital", 'building_type': 'Hospital', 'latitude': 29.86, 'longitude': 77.89, 'image_url': 'https://via.placeholder.com/300x200.png?text=Hospital'},
            {'building_name': f"Sharma Mishtan Bhandar {city_name}", 'building_type': 'Shop', 'latitude': 29.84, 'longitude': 77.87, 'image_url': 'https://via.placeholder.com/300x200.png?text=Mishtan+Bhandar'}
        ]
        return pd.DataFrame(fallback_data)

# Test karne ke liye
if __name__ == "__main__":
    fetcher = MapFetcher()
    df = fetcher.fetch_real_world_data("Roorkee")
    print(df.head())