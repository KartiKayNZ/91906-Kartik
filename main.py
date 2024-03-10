"""
Platformer Game
"""
import arcade
import time

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer"
PLAYER_START_X = 40
PLAYER_START_Y = 100

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
DASH_MULTIPLIER = 4


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


        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""


        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)


        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.scene.add_sprite("Player", self.player_sprite)
        
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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y += PLAYER_MOVEMENT_SPEED
    
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x += -PLAYER_MOVEMENT_SPEED
            
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED
            
        elif key == arcade.key.SPACE: 
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED*DASH_MULTIPLIER
            
        elif key == arcade.key.S:
            self.player_sprite.change_y += -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x -= -PLAYER_MOVEMENT_SPEED
            
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED
            
        elif key == arcade.key.SPACE:
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED*DASH_MULTIPLIER
            
        elif key == arcade.key.W:
            self.player_sprite.change_y -= PLAYER_MOVEMENT_SPEED      
        
        elif key == arcade.key.S:
            self.player_sprite.change_y -= -PLAYER_MOVEMENT_SPEED  


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
            
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y



        self.camera.move_to(player_centered)


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()