"""
Heart Soldiers, a top down game where you manouvre through levels
Each level is a different environment to find the things you need to find
"""

# Importing the libraries we need
import arcade
import math
import arcade.gui


# Window constants 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Heart Soldiers"

# The position where the player starts
PLAYER_START_X = 40
PLAYER_START_Y = 150
ENEMY_START_X = 2000
ENEMY_START_Y = 620

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 2
TILE_SCALING = 2
ENEMY_SCALING = 2
PORTAL_SCALING = 0.25

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_KNOCKBACK_SPEED = 15
ENEMY_MOVEMENT_SPEED = 4
ENEMY_KNOCKBACK_SPEED = 10
ENEMY_ATTACK = 50

# Shooting Constants
SPRITE_SCALING_LASER = 0.1
SHOOT_COOLDOWN = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

# Portal Spawn Positions 
PORTAL_SPAWN_X_L1 = 750
PORTAL_SPAWN_Y_L1 = 650

PORTAL_SPAWN_X_L2 = 1650
PORTAL_SPAWN_Y_L2 = 300

PORTAL_SPAWN_X_L3 = 650
PORTAL_SPAWN_Y_L3 = 650


# Layer name constants 
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_HEALTH_POT = "Health Pot"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_BULLETS = "Bullets"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_PORTAL = "Portal"
LAYER_NAME_ORBS = "Orbs"
LAYER_NAME_SWORD = "Sword"

# Direction List for player movement
direction = [0, 0]

# Value of health pot
HEALTH_POT_VALUE = 25

# Constants used to keep track of the player's current direction
'''RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3
IDLE_FACING = 4'''


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        # Current texture frame, alongside default direction 
        self.cur_texture = 0
        
        #self.scale = CHARACTER_SCALING
        #self.direction = "down"
        
        self.animation_timer = 0
        self.health = 100
        
        # asset path
        
        
class Enemy(Entity):
    def __init__(self):

        # Setup parent class
        super().__init__()

        self.scale = ENEMY_SCALING
        #main_path = "assets/ghost_sprites/ghost_mag.png"
        '''
        self.center_x = ENEMY_START_X
        self.center_y = ENEMY_START_Y
        '''
        
        self.attack = ENEMY_ATTACK
        
        main_path = "assets/ghost_sprites/ghost"
        
        self.idle_textures = []
                
        for i in range(5):
            self.idle_textures.append(arcade.load_texture(f"{main_path}_{i}.png"))
    
        self.texture = self.idle_textures[self.cur_texture]
        
    def update_animation(self, delta_time: float = 1 / 60):
        self.animation_timer += delta_time

        if self.animation_timer >= 0.15:
            self.animation_timer -= 0.15
            self.cur_texture += 1
            if self.cur_texture > 5:
                self.cur_texture = 0
        else:
            pass

class PlayerCharacter(Entity):
    """
    A class used for all attributes related to the player sprite
    """

    def __init__(self, game):
        '''
        This function is what is passed through when the player initialises. 
        This defines all the variables needed within the PlayerCharacter
        '''
        
        self.game = game
        
        # Set up parent class
        super().__init__()

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track the current state of what key is pressed
        '''self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False'''
        
        # Default character face direction
        self.direction = "down"
        
        # The animation timer to contorl the speed which the player animates
        self.animation_timer = 0

        # player assets
        main_path = "assets/player_sprites/player"

        
        
        '''YOU CAN CONDENSE THIS INTO LESS CODE MOST DEFINITELY'''
        
        
        
        # Load textures for idle standing
        self.idle_textures = {}
        for direction in ['up', 'down', 'left', 'right']:
            texture_pair = []
            for i in range(6):
                idle_texture = arcade.load_texture_pair(f"{main_path}_idle_{direction}_{i}.png")[0]
                texture_pair.append(idle_texture)
            self.idle_textures[direction] = texture_pair

        # Load textures for walking
        self.walk_textures = {}
        for direction in ['up', 'down', 'left', 'right']:
            texture_pair = []
            for i in range(6):
                walk_texture = arcade.load_texture_pair(f"{main_path}_walk_{direction}_{i}.png")[0]
                texture_pair.append(walk_texture)
            self.walk_textures[direction] = texture_pair
        
        
        # sword textures brokey
        self.sword_textures = {}
        for direction in ['up', 'down', 'left', 'right']:
            texture_pair = []
            for i in range(6):
                sword_texture = arcade.load_texture_pair(f"{main_path}_swing_{direction}_{i}.png")[0]
                texture_pair.append(sword_texture)
            self.sword_textures[direction] = texture_pair
        
        # Set the initial texture
        self.texture = self.idle_textures[self.direction][self.cur_texture]
    def update_animation(self, delta_time: float = 1 / 60):
        '''
        This function is dedicated to updating animations in the code
        This is passed through on_update() to update every frame
        '''
    
        
        self.animation_timer += delta_time
        #print(self.game.swing)
        
        '''if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction][self.cur_texture]
            #print("line 153 stationary")'''
        
        if self.game.swing == True:
            self.texture = self.sword_textures[self.direction][self.cur_texture]
        elif self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction][self.cur_texture]
        else:
            self.texture = self.walk_textures[self.direction][self.cur_texture]
            
        
        
        
        if self.change_x < 0:
            self.direction = 'left'
        elif self.change_x > 0:
            self.direction = 'right'

        if self.change_y > 0:
            self.direction = 'up'
        elif self.change_y < 0:
            self.direction = 'down'
        
        if self.game.swing == True:
            print(self.cur_texture)
            if self.animation_timer >= 0.08:
                self.animation_timer -= 0.08
                self.cur_texture += 1
                if self.cur_texture > 5:
                    self.cur_texture = 0
                    self.game.swing = False
        
        if self.game.swing == False:
            if self.animation_timer >= 0.08:
                self.animation_timer -= 0.08
                self.cur_texture += 1
                if self.cur_texture > 5:
                    self.cur_texture = 0
        

                    
        else:
            pass
        
        
class QuitButton(arcade.gui.UIFlatButton):
    '''
    This class is for the Quit button on the MainMenu menu
    '''
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        '''
        If the button is clicked, then the code will quit
        '''
        arcade.exit()
        
class StartButton(arcade.gui.UIFlatButton):
    '''
    This class is for the start button on the MainMenu
    '''
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        '''
        If the code is clicked, then this will close the MainMenu window, then
        run the actual arcade window with the game in it
        '''
        # Getting the current arcade window
        window = arcade.get_window()
        # This is setting the GameView (the actual game) to a view of the GameView class??
        game_view = GameView()
        # This shows the load screen
        # Game_view.setup() just runs the setup of the GameView() 
        game_view.setup()
        # And then this window just changes the view to the actual game. 
        window.show_view(game_view)
        
class MainMenu(arcade.View):
    """The main menu of the game"""

    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.label = arcade.Text(
            SCREEN_TITLE,
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-200,
            arcade.csscolor.WHITE,
            70,
            anchor_x="center",
            font_name=("Kenney Pixel Square"),
        )
        
        self.instructions = arcade.Text(
            'To play, WASD or Arrow Keys to move. E is to swing your sword',
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-260,
            arcade.csscolor.WHITE,
            20,
            anchor_x="center",
            font_name=("Arial"),
        )
        
        # Set background color
        arcade.set_background_color(arcade.color.BLAST_OFF_BRONZE)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = StartButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Again, method 1. Use a child class to handle events.
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.label.draw()
        self.instructions.draw()

class EndMenu(arcade.View):
    def __init__(self, time_completed = 0):
        super().__init__()
        game = GameView()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.DARK_GREEN)
        
        self.v_box = arcade.gui.UIBoxLayout()
        
        self.finish_text = arcade.Text(
            f'You finished the game! Well done!',
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT - 150,
            arcade.csscolor.WHITE,
            18,
            anchor_x= "center",
            
        )
        
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child = self.v_box)
        )
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.finish_text.draw()

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Our Scene Object
        self.scene = None

        self.can_shoot = False
        
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None
        self.gui_camera = None
        
        #Enemy health
        self.enemy_health = 0

        #Enemy attack
        self.enemy_attack = ENEMY_ATTACK

        #Enemy following player
        self.enemy_follow = True
        
        self.enemy_can_attack = False
        
        self.dashing = None
        
        self.invincible = None
        self.invincible_time = 0
        
        self.knockback = None
        self.knockback_time = 0
        self.enemy_knockback = False
        
        self.portal_enter = None
        
        self.shoot_pressed = False    
        
        self.player_direction = None
        
        self.portal_spawn_x = 0
        self.portal_spawn_y = 0
            
        # Do we need to reset the score?
        self.reset_score = True

        self.sword_collected = False
        
        self.level = 1
        
        self.enemy_spawn = None
            
        self.quest_text = ""
        
        self.level_quest = ""
        
        self.orbs_collected = 0
        
        self.level_complete = None
        
        self.shoot_available = None
        
        # Keep track of the score
        self.score = 0
        
        # Keeps track of the player's health
        self.health = 100
        
        self.enemy_dead = False
        
        self.up_pressed = None
        self.down_pressed = None
        self.left_pressed = None
        self.right_pressed = None
        
        self.swing = False
        
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound("assets/hurt.mp3")
        self.heal_sound = arcade.load_sound("assets/heal.mp3")
        self.yay_sound = arcade.load_sound("assets/yay.mp3")
        
        self.score_text = arcade.Text(
            '',
            1000,
            660,
            arcade.csscolor.WHITE,
            18,
            font_name=("Kenney Mini Square")
            
        )
        
        self.health_text = arcade.Text(
            '',
            1000,
            680,
            arcade.csscolor.WHITE,
            18,
            font_name=("Kenney Mini Square"),
            
        )
        
        self.enemy_health_text = arcade.Text(
            '',
            1000,
            640,
            arcade.csscolor.WHITE,
            18,
            font_name=("Kenney Mini Square"),
        )
        
        self.quest_text = arcade.Text(
            '',
            10,
            680,
            arcade.csscolor.WHITE,
            18,
            font_name=("Comic Sans MS","Kenney Blocks"),
        )
        
        
        

        arcade.set_background_color((234, 165, 108))
        
        self.timer = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.enemy_sprite = Enemy()
        
        if self.level == 3:
            self.enemy_spawn = True
            self.enemy_can_attack = True
        else:
            self.enemy_spawn = False
            self.enemy_can_attack = False
        
        
        self.swing = False
        
        # Set up the Camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Name of map file to load
        map_name = f"maps/level_{self.level}.tmx"            
        
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
            LAYER_NAME_ORBS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_SWORD: {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter(self)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)
        
        
        
        
        '''IS THIS CORRECT'''
        
        if self.enemy_spawn == True:
            #Enemy sprite
            self.enemy_sprite.center_x = ENEMY_START_X
            self.enemy_sprite.center_y = ENEMY_START_Y
            self.scene.add_sprite(LAYER_NAME_ENEMIES, self.enemy_sprite)
        
        
        
        
            
        # Shooting mechanics
        self.shoot_available = False
        self.can_shoot = True
        self.shoot_timer = 0
        
        self.score = 0
        # Making sure level not complte
        self.level_complete = False
        
        self.enemy_health = 100

        self.portal_sprite = None
        
        self.portal_enter = False
        #so bullets have a home
        #self.bullet_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Create the 'physics engine'
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene["Walls"]
            )
        
        self.player_direction = self.player_sprite.direction
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        
        self.gui_camera.use()
        
        self.health_text.draw()
        self.score_text.draw()
        self.enemy_health_text.draw()
        self.quest_text.draw()
        
        
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
        elif key == arcade.key.E:
            self.shoot_pressed = True

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
        elif key == arcade.key.E:
            self.shoot_pressed = False
        
        
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
    
    '''def attack(self, game):
        enemy = self.enemy_sprite  # Get the enemy sprite'''
    
    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update the player's animation
        self.player_sprite.update_animation(delta_time)
        self.enemy_sprite.update_animation(delta_time)

        # Position the camera
        self.center_camera_to_player()
        

        '''player_collision_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_BULLETS]
            ]
        )'''
        
        pot_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_HEALTH_POT]
        )

        # Loop through each health pot we hit (if any) and remove it
        for pot in pot_hit_list:
            pot.remove_from_sprite_lists()
            self.health += HEALTH_POT_VALUE
            arcade.play_sound(self.heal_sound)
            
        self.scene.update_animation(
            delta_time, [LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
        )
        
        
        orb_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_ORBS]
        )

        # Loop through each orb we hit (if any) and remove it
        for orb in orb_hit_list:
            orb.remove_from_sprite_lists()
            self.orbs_collected += 1
            #arcade.play_sound(self.heal_sound)
        
        sword_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_SWORD]
        )

        # Loop through each health pot we hit (if any) and remove it
        for sword in sword_hit_list:
            sword.remove_from_sprite_lists()
            self.sword_collected = True
            arcade.play_sound(self.heal_sound)
            
        if self.sword_collected == True:
            if self.level == 2:
                self.level_complete = True
            self.shoot_available = True
            
        
            
        self.scene.update_animation(
            delta_time, [LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
        )
        
        
        ###ENEMY FOLLOWING PLAYER###
        
        if self.enemy_can_attack == True:
                
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
                    self.player_sprite.center_x += math.cos(angle) * PLAYER_KNOCKBACK_SPEED
                    self.player_sprite.center_y += math.sin(angle) * PLAYER_KNOCKBACK_SPEED
                    self.enemy_sprite.change_x -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                    self.enemy_sprite.change_y -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                    
                    self.knockback_time += 1
                if self.knockback_time == 5:
                    self.knockback = False

        #WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP    
        '''if self.enemy_knockback == True:
            if self.knockback_time < 5:
                self.enemy_sprite.change_x -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                self.enemy_sprite.change_y -= math.sin(angle) * ENEMY_KNOCKBACK_SPEED
                self.knockback_time += 1
            if self.knockback_time == 5:
                self.enemy_knockback = False'''
            
        
        #Sets how long the invincible period is
        if self.invincible == True:
            if self.invincible_time < 60:
                self.invincible = True
                self.invincible_time += 1
            if self.invincible_time == 60:
                self.invincible = False
                self.invincible_time = 0
    
    
        if self.shoot_available == True:
            if self.can_shoot:
                if self.shoot_pressed:
                    self.swing = True
                    print("self.swing is set to true now")
                    arcade.play_sound(self.shoot_sound)
                    bullet = arcade.Sprite(
                        "assets/player_sprites/sword_slash.png",
                        SPRITE_SCALING_LASER,
                    )
                    self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)
                    bullet.center_x = self.player_sprite.center_x
                    bullet.center_y = self.player_sprite.center_y

                    
                    if self.player_sprite.direction == 'left':
                        bullet.change_x = -BULLET_SPEED
                    elif self.player_sprite.direction == 'right':
                        bullet.change_x = BULLET_SPEED
                    if self.player_sprite.direction == 'up':
                        bullet.change_y = BULLET_SPEED
                    elif self.player_sprite.direction == 'down':
                        bullet.change_y = -BULLET_SPEED


                    #self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                    self.can_shoot = False
                
            else:
                self.shoot_timer += 1
                if self.shoot_timer == SHOOT_COOLDOWN:
                    self.can_shoot = True
                    self.shoot_timer = 0
        else:
            #print("not able to shoot dont have sword")
            pass
        
        if self.health <= 0:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.enemy_sprite.center_x = ENEMY_START_X
            self.enemy_sprite.center_y = ENEMY_START_Y
            self.health = 100
            
        
        # Update the bullet sprites
        
        for bullet in self.scene[LAYER_NAME_BULLETS]:
            '''This should change to colission with lists when you add more '''
            if self.level == 3:
                hit_list = arcade.check_for_collision_with_lists(
                    bullet,
                    [
                        self.scene[LAYER_NAME_ENEMIES]
                    ],
                )
            

                if hit_list:
                    for collision in hit_list:
                        if self.enemy_sprite == collision:
                            self.enemy_knockback = True
                            self.enemy_health -= BULLET_DAMAGE
                            arcade.play_sound(self.hit_sound)
                            if self.enemy_health <= 0:
                                collision.remove_from_sprite_lists()
                                self.enemy_can_attack = False
                                arcade.play_sound(self.yay_sound)
                                self.enemy_dead = True
                                self.level_complete = True

                            
                        else:
                            print("Meow")
                            
                            

                    bullet.remove_from_sprite_lists()
            else:
                pass
            bullet.update()
             
        
        for bullet in self.scene[LAYER_NAME_BULLETS]:
            bullet.update()
        
        if self.level == 1:
            self.level_quest = f"Find all 3 orbs, to summon the portal\nOrbs collected: {self.orbs_collected}"
        elif self.level == 2:
            self.level_quest = "Find a weapon, you'll need it..."
        elif self.level == 3:
            self.level_quest = "You've angered the ghosts. Brace yourself."
        else:
            self.level_quest = "ERROR"
        
        
        
        # Update score text
        self.score_text.text = f"Score: {self.score}"
        self.health_text.text = f"Health: {self.health}"
        self.enemy_health_text.text = f"Enemy Health: {self.enemy_health}"
        self.quest_text.text = f"Quest: {self.level_quest}"
        
        
        # Boundary Code
        if self.player_sprite.center_x > 2550:
            self.player_sprite.change_x = -5
        elif self.player_sprite.center_x < 0:
            self.player_sprite.change_x = 5
            
        if self.player_sprite.center_y > 1425:
            self.player_sprite.change_y = -5
        elif self.player_sprite.center_y < 0:
            self.player_sprite.change_y = 5

        
        if self.level_complete == True:
            if self.portal_sprite is None:
                # Portal sprite
                portal_img = "assets/portal_sprites/portal_0.png"
                self.portal_sprite = arcade.Sprite(portal_img, PORTAL_SCALING)
                
                # FIX THIS LATER
                if self.level == 1:
                    self.portal_spawn_x = PORTAL_SPAWN_X_L1
                    self.portal_spawn_y = PORTAL_SPAWN_Y_L1
                elif self.level == 2:
                    self.portal_spawn_x = PORTAL_SPAWN_X_L2
                    self.portal_spawn_y = PORTAL_SPAWN_Y_L2
                elif self.level == 3:
                    self.portal_spawn_x = PORTAL_SPAWN_X_L3
                    self.portal_spawn_y = PORTAL_SPAWN_Y_L3
                else: 
                    print("OUT OF RANGE LEVELS")
                
                self.portal_sprite.center_x = self.portal_spawn_x
                self.portal_sprite.center_y = self.portal_spawn_y 
                self.scene.add_sprite(LAYER_NAME_PORTAL, self.portal_sprite)
                print(len(self.scene[LAYER_NAME_PORTAL]))
            portal_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_PORTAL]
            )
            
            for portal in portal_hit_list:
                portal.remove_from_sprite_lists()
                self.portal_enter = True
                print("PORTAL HAS BEEN DELETED ")
        
                
        elif self.level_complete == False:
            pass
        else:
            print("chat how did we get here")
        
        if self.orbs_collected == 3 and self.level == 1:
            self.level_complete = True
        
        if self.portal_enter == True:
            if self.enemy_dead == True:
                # add the window here
                end_view = EndMenu(self.timer)
                self.window.show_view(end_view)
                
            else:   
                self.level += 1
                self.setup()
                self.portal_enter = False
                print(self.level_complete)

        #FPS
        #print(1/delta_time)
        if self.enemy_dead == False:
            self.timer += delta_time
        
            
                
            
            
def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window = True)
    window.show_view(MainMenu())
    arcade.run()


if __name__ == "__main__":
    main()