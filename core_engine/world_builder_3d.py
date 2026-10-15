# ==========================================
# World Builder 3D - CityCore-3D
# Author: Vansh Gupta
# Yeh file Ursina engine se 3D city render karegi,
# player ki body, day-night environment aur 
# Blueprint/X-Ray mode ko sambhalegi.
# ==========================================

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class CityWorld3D:
    def __init__(self):
        # Ursina app start kar rahe hain bhai
        self.app = Ursina()
        
        # Window ki basic settings taaki game professional lage
        window.title = "CITYCORE-3D: Smart City Simulation Engine"
        window.borderless = False
        window.fullscreen = False
        window.exit_button.enabled = False
        window.fps_counter.enabled = True

        # R रोशनी aur aasmaan ka setup
        self.setup_environment()
        
        # Player controller aur uski body ka setup
        self.setup_player()
        
        # Building entities ki list
        self.buildings = []
        self.is_blueprint_mode = False

    def setup_environment(self):
        # Subah ka khubsurat neela aasmaan (Skybox)
        self.sky = Sky(color=color.rgb(135, 206, 235))
        
        # Directional light taaki buildings par shadow aur depth aaye
        self.dir_light = DirectionalLight(y=2, z=3, shadows=True)
        self.ambient = AmbientLight(color=color.rgba(150, 150, 150, 255))

    def setup_player(self):
        # WASD se ghumne ke liye player controller
        self.player = FirstPersonController(y=2, speed=10)
        self.player.cursor.enabled = True 
        
        # Player ki apni body ka block (Taki third-person/visible feel aaye)
        self.player_body = Entity(
            parent=self.player,
            model='cube',
            color=color.orange,
            scale=(0.8, 1.8, 0.5),
            position=(0, -0.5, 0)
        )
        print("--> Player body aur movement controls tayar hain!")

    def build_city_grid(self, df_buildings):
        # Zameen (Ground plane) jiske upar poora shehar basega
        self.ground = Entity(
            model='plane',
            scale=(300, 1, 300),
            color=color.rgb(40, 40, 40),
            texture='white_cube',
            collider='box'
        )

        # DataFrame se ek-ek building ko 3D world mein utaar rahe hain
        for index, row in df_buildings.iterrows():
            b_name = row['building_name']
            b_type = row['building_type']
            x = row['coordinate_x']
            z = row['coordinate_z']

            # Building ke type ke hisab se color aur size set karenge
            if 'Hospital' in b_type:
                b_color = color.rgb(220, 50, 50)  # Asli laal hospital feel
                b_scale = (5, 7, 5)
            elif 'Shop' in b_type or 'Commercial' in b_type:
                b_color = color.rgb(0, 180, 216)  # Chamakta hua cyan commercial color
                b_scale = (4, 5, 4)
            elif 'Residential' in b_type:
                b_color = color.rgb(76, 201, 240) # Residential sky blue
                b_scale = (5, 9, 5)
            else:
                b_color = color.rgb(247, 127, 0)  # Landmarks ke liye orange tone
                b_scale = (4, 6, 4)

            # 3D Building Entity create karo
            b_entity = Entity(
                model='cube',
                color=b_color,
                scale=b_scale,
                position=(x, b_scale[1]/2, z),
                collider='box'
            )
            
            # Click detection ke liye naam aur type attach kar rahe hain
            b_entity.building_name = b_name
            b_entity.building_type = b_type
            
            self.buildings.append(b_entity)
        
        print(f"--> Wah bhai! Total {len(self.buildings)} buildings 3D world mein successfully render ho gayi hain.")

    def input(self, key):
        # Keyboard shortcuts
        if key == 'b':
            self.toggle_blueprint_mode()
        
        # Jab user kisi building par click karega (Raycasting magic)
        if key == 'left mouse down':
            hit_info = mouse.entity
            if hit_info and hasattr(hit_info, 'building_name'):
                print(f"\n--- [LIVE BUILDING POPUP CLICKED] ---")
                print(f"Name : {hit_info.building_name}")
                print(f"Type : {hit_info.building_type}")
                print(f"Status: Active & Connected to Database/Matplotlib Graph.")
                print(f"--------------------------------------\n")

    def toggle_blueprint_mode(self):
        # Press 'B' to toggle futuristic CAD Blueprint / X-Ray Mode
        self.is_blueprint_mode = not self.is_blueprint_mode
        
        if self.is_blueprint_mode:
            print("--> X-Ray CAD Blueprint Mode On!")
            self.sky.color = color.rgb(10, 25, 60) # Dark blueprint blue background
            for b in self.buildings:
                b.color = color.rgb(0, 162, 232)   # Blueprint glowing cyan lines look
        else:
            print("--> Normal Textured World Mode On!")
            self.sky.color = color.rgb(135, 206, 235)
            for b in self.buildings:
                b.color = color.gray # Wapas normal color

    def run(self):
        self.app.run()

# Test karne ke liye agar direct run karein
if __name__ == "__main__":
    import pandas as pd
    sample_df = pd.DataFrame([
        {'building_name': 'Civil Lines Central Chowk', 'building_type': 'Landmark', 'coordinate_x': 5, 'coordinate_z': 10},
        {'building_name': 'Roorkee City Hospital', 'building_type': 'Hospital', 'coordinate_x': -12, 'coordinate_z': 15},
        {'building_name': 'Sharma Mishtan Bhandar', 'coordinate_x': 15, 'coordinate_z': -10, 'building_type': 'Shop'}
    ])
    
    world = CityWorld3D()
    world.build_city_grid(sample_df)
    world.run()