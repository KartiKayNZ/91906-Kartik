"""
Platformer Game
"""
import arcade
import time




SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer"

# The position where the player starts
PLAYER_START_X = 40
PLAYER_START_Y = 100

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.75
TILE_SCALING = 2

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
PLAYER_DASH_SPEED = 20
GRAVITY = 1
DASH_MULTIPLIER = 4

# Layer names from the tiled map
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_HEALTH_POT = "Health Pot"
LAYER_NAME_TRACKS = "Tracks"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DOORS = "Doors"
LAYER_NAME_ENEMIES = "Enemies"

# Direction List
direction = [0, 0]



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        self.dashing = None
        
        self.dashtime = 10
        
        # Do we need to reset the score?
        self.reset_score = True

        # Keep track of the score
        self.score = 0
        
        # Keeps track of the player's health
        self.health = 100
        
        self.up_pressed = None
        self.down_pressed = None
        self.left_pressed = None
        self.right_pressed = None

        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        
        score_text = f"Health: {self.health}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        
        arcade.set_background_color((234, 165, 108))

    def setup(self):
        """Set up the game here. Call this function to restart the game."""


        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)
        

        # Name of map file to load
        map_name = "maps/level_1_big.tmx"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_HEALTH_POT: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DOORS:{
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.scene.add_sprite("Player", self.player_sprite)
        
        # Create the 'physics engine'
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene["Walls"]
        )

        
        
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            680,
            arcade.csscolor.WHITE,
            18,
        )
        
        score_text = f"Health: {self.health}"
        arcade.draw_text(
            score_text,
            10,
            700,
            arcade.csscolor.WHITE,
            18,
        )

    def update_player_speed(self):
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            direction[0] = 1
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            direction[0] = -1
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            direction[1] = -1
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            direction[1] = 1

        if self.right_pressed and self.left_pressed:
            self.player_sprite.change_x = 0
            direction[1] = 0
        if self.up_pressed and self.down_pressed:
            self.player_sprite.change_y = 0
            direction[0] = 0
            
        if not self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = 0
            direction[1] = 0
        if not self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = 0
            direction[0] = 0

    def on_key_press(self, key, modifiers):
        """When a key is pressed/held down."""

        if key == arcade.key.SPACE:
            self.dashing = True
            
        if key == arcade.key.W: 
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """When a held key is released."""

        if key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()
        elif key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        
        if screen_center_y < 0:
            screen_center_y = 0
            
        if screen_center_x >= 1280:
            screen_center_x = 1280
        if screen_center_y >= 720:
            screen_center_y = 720

        player_centered = screen_center_x, screen_center_y



        self.camera.move_to(player_centered)


    def on_update(self, delta_time):
        """Movement and game logic"""

        '''if self.dashing == True:
            self.player_sprite.change_y = PLAYER_DASH_SPEED * direction[1]
            self.player_sprite.change_x = PLAYER_DASH_SPEED * direction[0]
            self.dashtime += 1
            if self.dashtime == 10:
                self.dashing = False
                self.dash_start = 0
                if self.dashing == True:
                    self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED * direction [0]
                    self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * direction [1]'''
            
        
        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()
        
        pot_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Health Pot"]
        )

        # Loop through each coin we hit (if any) and remove it
        for pot in pot_hit_list:
    
            # Figure out how many points this coin is worth
            if "health" not in pot.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                health = int(pot.properties["health"])
                self.health += health
                print(self.health)

            # Remove the coin
            pot.remove_from_sprite_lists()
            
            
            '''#ADD A HEAL NOISE!!!!!!!!!!!!!!'''
            
            #arcade.play_sound(self.heal_noise)
        if self.player_sprite.center_x > 2550:
            self.player_sprite.change_x = -5
        elif self.player_sprite.center_x < 0:
            self.player_sprite.change_x = 5
            
        if self.player_sprite.center_y > 1425:
            self.player_sprite.change_y = -5
        elif self.player_sprite.center_y < 0:
            self.player_sprite.change_y = 5
            
        

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()