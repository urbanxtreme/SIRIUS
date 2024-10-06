from ursina import *
import math

# Global variable to track the time for orbiting planets
t = 0

class SolarSystem(Entity):
    def __init__(self):
        super().__init__()

        # Create the sun
        self.sun = Entity(model='sphere', scale=1.5, color=color.yellow)

        # Create planets
        self.planets = [
            Entity(model='sphere', scale=0.1, color=color.gray, position=(3, 0, 0), parent=self.sun),   # Mercury
            Entity(model='sphere', scale=0.2, color=color.orange, position=(4, 0, 0), parent=self.sun),  # Venus
            Entity(model='sphere', scale=0.3, color=color.blue, position=(5, 0, 0), parent=self.sun),    # Earth
            Entity(model='sphere', scale=0.15, color=color.red, position=(6, 0, 0), parent=self.sun),     # Mars
            Entity(model='sphere', scale=0.5, color=color.brown, position=(7, 0, 0), parent=self.sun),   # Jupiter
            Entity(model='sphere', scale=0.4, color=color.orange, position=(8, 0, 0), parent=self.sun),  # Saturn
            Entity(model='sphere', scale=0.35, color=color.cyan, position=(9, 0, 0), parent=self.sun),   # Uranus
            Entity(model='sphere', scale=0.35, color=color.blue, position=(10, 0, 0), parent=self.sun),   # Neptune
        ]

    def update(self):
        global t
        t += time.dt

        # Orbiting planets
        for i, planet in enumerate(self.planets):
            radius = planet.position.x
            planet.x = radius * math.cos(t + i)
            planet.z = radius * math.sin(t + i)

class Sky(Entity):
    def __init__(self):
        super().__init__(model='sphere', scale=150, color=color.black, double_sided=True)

def update():
    # Control the camera movement
    if held_keys['w']:
        camera.position += camera.forward * 0.1
    if held_keys['s']:
        camera.position -= camera.forward * 0.1
    if held_keys['a']:
        camera.position -= camera.right * 0.1
    if held_keys['d']:
        camera.position += camera.right * 0.1
    if held_keys['q']:
        camera.position += camera.up * 0.1
    if held_keys['e']:
        camera.position -= camera.up * 0.1

# Create the application
app = Ursina()

# Add skybox
sky = Sky()

# Create the solar system
solar_system = SolarSystem()

# Set the initial camera position
camera.position = (0, 5, -15)
camera.rotation_x = 20

# Run the application
app.run()
