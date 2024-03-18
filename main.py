"""
Platformer Game
"""
import arcade
import time
import math
import random




SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer"

# The position where the player starts
PLAYER_START_X = 40
PLAYER_START_Y = 100

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 2
TILE_SCALING = 2
ENEMY_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_DASH_SPEED = 15
GRAVITY = 1
DASH_MULTIPLIER = 4
ENEMY_MOVEMENT_SPEED = 4
ENEMY_KNOCKBACK_SPEED = 10


# Layer names from the tiled map
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_HEALTH_POT = "Health Pot"
LAYER_NAME_TRACKS = "Tracks"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DOORS = "Doors"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_PLAYER = "Player"

# Direction List
direction = [0, 0]

# Value of health pot
HEALTH_POT_VALUE = 25

# Constants used to keep track of the player's current direction
RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3
IDLE_FACING = 4

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = IDLE_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # --- Load Textures ---

        # player assets
        main_path = "assets/player_sprites/player"

        # Load textures for idle standing
        self.idle_textures = []
        for i in range(6):
            idle_texture = arcade.load_texture_pair(f"{main_path}_idle_{i}.png")[0]
            self.idle_textures.append(idle_texture)

        # Load textures for walking
        self.walk_textures = {}
        for direction in ['up', 'down', 'left', 'right']:
            texture_pair = []
            for i in range(6):
                walk_texture = arcade.load_texture_pair(f"{main_path}_walk_{direction}_{i}.png")[0]
                texture_pair.append(walk_texture)
            self.walk_textures[direction] = texture_pair
        # Set the initial texture
        self.texture = self.idle_textures[0]


    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.character_face_direction]
            return

        direction = ''
        if self.change_x < 0:
            direction = 'left'
        elif self.change_x > 0:
            direction = 'right'

        if self.change_y > 0:
            direction = 'up'
        elif self.change_y < 0:
            direction = 'down'

        self.cur_texture += 1
        if self.cur_texture > 5:
            self.cur_texture = 0

        self.texture = self.walk_textures[direction][self.cur_texture]

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
        
        #Enemy health
        self.enemy_max_health = 20
        self.enemy_health = 20

        #Enemy attack
        self.enemy_attack = 5

        #Enemy following player
        self.enemy_follow = True
        
        self.dashing = None
        
        self.dashtime = 10
        
        self.invincible = None
        self.invincible_time = 0
        
        self.knockback = None
        self.knockback_time = 0
        
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
        
        self.heal_sound = arcade.load_sound("assets/heal.mp3")
        
        
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

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Player")
        
        #Enemy sprite
        enemy_img = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        self.enemy_sprite = arcade.Sprite(enemy_img, ENEMY_SCALING)
        self.enemy_sprite.center_x = 400
        self.enemy_sprite.center_y = 450
        self.scene.add_sprite("Enemy", self.enemy_sprite)
        
        
        
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

    def process_keychange(self):
        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
        
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_y = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

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

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update the player's animation
        self.player_sprite.update_animation(delta_time)

        # Position the camera
        self.center_camera_to_player()

        # ... rest of the code ...
        
        pot_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Health Pot"]
        )

        # Loop through each coin we hit (if any) and remove it
        for pot in pot_hit_list:
    
            '''# Figure out how many points this coin is worth
            if "heal" not in pot.properties:
                print("Warning, collected a heatlh pot without a health property.")
            else:
                health = int(pot.properties["heal"])
                self.health += health
                print(self.health)'''
            # Remove the coin
            pot.remove_from_sprite_lists()
            self.health += HEALTH_POT_VALUE
            arcade.play_sound(self.heal_sound)
            
        self.scene.update_animation(
            delta_time, [LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
        )
        
        ###ENEMY FOLLOWING PLAYER###
            
        #Enemy following player
        self.enemy_sprite.center_x += self.enemy_sprite.change_x
        self.enemy_sprite.center_y += self.enemy_sprite.change_y

        #Records the enemy's position
        start_x = self.enemy_sprite.center_x
        start_y = self.enemy_sprite.center_y

        #Records the player's position
        dest_x = self.player_sprite.center_x
        dest_y = self.player_sprite.center_y

        #Calculates the x and y distance between the enemy and the player
        dist_x = int(dest_x - start_x)
        dist_y = int(dest_y - start_y)
        #Using trig to find the angle difference between the player and enemy
        angle = math.atan2(dist_y, dist_x)
        
        #Checks for collision between the player and enemy
        if self.invincible != True:
            enemy_collision = arcade.check_for_collision(self.player_sprite, self.enemy_sprite)
        else:
            enemy_collision = False

        #Making the enemy follow the player precicely using trig
        if self.enemy_follow == True:
            self.enemy_sprite.change_x = math.cos(angle) * ENEMY_MOVEMENT_SPEED
            self.enemy_sprite.change_y = math.sin(angle) * ENEMY_MOVEMENT_SPEED
        #Stops the enemy if there is collision
        elif self.enemy_follow == False:
            self.enemy_sprite.change_x = 0
            self.enemy_sprite.change_y = 0
            
        #Creates player knockback if enemy collides with the player
        if enemy_collision == True:
            self.health -= self.enemy_attack
            self.knockback_time = 0
            self.knockback = True
            self.invincible = True
        
        #Sets how far the knockback is going to be
        if self.knockback == True:
            if self.knockback_time < 5:
                self.player_sprite.center_x += math.cos(angle) * PLAYER_DASH_SPEED
                self.player_sprite.center_y += math.sin(angle) * PLAYER_DASH_SPEED
                self.enemy_sprite.change_x -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                self.enemy_sprite.change_y -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                
                self.knockback_time += 1
            if self.knockback_time == 5:
                self.knockback = False

        #Sets how long the invincible period is
        if self.invincible == True:
            if self.invincible_time < 60:
                self.invincible = True
                self.invincible_time += 1
            if self.invincible_time == 60:
                self.invincible = False
                self.invincible_time = 0


        
        
            
        # Boundary code 
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