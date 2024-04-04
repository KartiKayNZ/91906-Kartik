"""
Heart Soldiers, a top down game where you manouvre through levels
Each level is a different environment to find the things you need to find.
"""

# Importing the libraries I need.
import arcade
import math
import arcade.gui
from itertools import cycle

# Window constants.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Heart Soldiers"

# The position where the player starts.
PLAYER_START_X = 80
PLAYER_START_Y = 200
ENEMY_START_X = 2000
ENEMY_START_Y = 620

# Constants used to scale our sprites from their original size.
CHARACTER_SCALING = 2
TILE_SCALING = 2
ENEMY_SCALING = 2
PORTAL_SCALING = 0.25
SLASH_SCALING = 0.1

# Animation constants related to the animations in the game.
ANIMATION_SPEED = 0.15
SWORD_ANIMATION_SPEED = 0.08
PLAYER_FRAME_COUNT = 6

# Maximum Knockback Time.
MAX_KNOCKBACK_TIME = 5

# Movement speed of player, in pixels per frame.
PLAYER_MOVEMENT_SPEED = 10
PLAYER_KNOCKBACK_SPEED = 30
ENEMY_MOVEMENT_SPEED = 3
ENEMY_KNOCKBACK_SPEED = 10
ENEMY_ATTACK = 25

# Shooting Constants.
SHOOT_COOLDOWN = 30
SLASH_SPEED = 12
SLASH_DAMAGE = 25

# Portal Spawn Positions.
PORTAL_SPAWN_X_L1 = 750
PORTAL_SPAWN_Y_L1 = 650
PORTAL_SPAWN_X_L2 = 1650
PORTAL_SPAWN_Y_L2 = 300
PORTAL_SPAWN_X_L3 = 650
PORTAL_SPAWN_Y_L3 = 650

# Layer name constants.
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_HEALTH_POT = "Health Pot"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_SLASHS = "Slashs"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_PORTAL = "Portal"
LAYER_NAME_ORBS = "Orbs"
LAYER_NAME_SWORD = "Sword"



MAX_INVINCIBLE_TIME = 30
DIRECTIONS = ["up", "down", "left", "right"]
# Direction List for player movement.
direction = [0, 0]

# Player and enemy health values.
PLAYER_HEALTH = 100

# Item constants.
HEALTH_POT_VALUE = 25
MAX_ORBS = 3

# Level constants.
LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3


def load_texture_dict(path, frame_count, directions):
    ''' This function loads the textures for each
    direction and frame.'''
    
    # Creates a texture dictionary, then loads each direction's texture
    # then appends the texture list to the texture dictionary with the
    # appropriate direction. 
    textures = {}
    for direction in directions:
        texture_list = []
        for i in range(frame_count):
            texture = arcade.load_texture(f"{path}_{direction}_{i}.png")
            texture_list.append(texture)
        textures[direction] = texture_list
    # Returns the texture dictionary.
    return textures

class Entity(arcade.Sprite):
    ''' This is the base entity class for the game. 
        All entities in the game inherit from this class.'''
    def __init__(self):
        ''' This is the constructor for the Entity class. '''
        
        # Setup parent class.
        super().__init__()
        
        # Current texture frame, alongside default direction.
        self.cur_texture = 0
        
        # The timer that allows for animation speed control.
        self.animation_timer = 0
        
        # Default health of each entity.
        self.health = 100
        
        
        
class EnemyCharacter(Entity):
    ''' This is the enemy code. This code inherits from the Entity class.
    and '''
    def __init__(self):

        # Setup parent class.
        super().__init__()
        
        # Scaling of the enemy sprite.
        self.scale = ENEMY_SCALING

        # The amount of damage the enemy does to the player.
        self.attack = ENEMY_ATTACK
        
        # The main path where ghost assets are found.
        main_path = "assets/ghost_sprites/ghost"
        
        # Creating an idle textures list.
        self.idle_textures = []
        
        # FIX THIS AND COMMENT
        for i in range(5):
            self.idle_textures.append\
(arcade.load_texture(f"{main_path}_{i}.png"))
    
        self.texture = self.idle_textures[self.cur_texture]
        
    def update_animation(self, delta_time: float = 1 / 60):
        self.animation_timer += delta_time

        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer -= ANIMATION_SPEED
            self.cur_texture += 1
            if self.cur_texture > 5:
                self.cur_texture = 0
        else:
            pass

class PlayerCharacter(Entity):
    """
    A class used for all attributes related to the player sprite.
    """

    def __init__(self, game):
        '''
        This function is what is passed through when the player
        initialises. This defines all the variables
        needed within the PlayerCharacter.
        '''
        
        # Setting self.game = to game in order to check the state of 
        # game attributes.
        self.game = game
        
        # Set up parent class.
        super().__init__()

        # Used for flipping between image sequences.
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        
        # Default character face direction.
        self.direction = "down"
        
        # The animation timer to contorl the speed which the 
        # player animates.
        self.animation_timer = 0


        # Path to the player assets
        main_path = "assets/player_sprites/player"

        
        
        '''YOU CAN CONDENSE THIS INTO LESS CODE MOST DEFINITELY'''
        
        '''YOU CAN CONDENSE THIS INTO LESS CODE MOST DEFINITELY'''
        '''YOU CAN CONDENSE THIS INTO LESS CODE MOST DEFINITELY'''
        
        # Load idle, walk and sword textures.
        main_path = "assets/player_sprites/player_"
        self.idle_textures = load_texture_dict(f"{main_path}idle", PLAYER_FRAME_COUNT, DIRECTIONS)
        self.walk_textures = load_texture_dict(f"{main_path}walk", PLAYER_FRAME_COUNT, DIRECTIONS)
        self.sword_textures = load_texture_dict(f"{main_path}swing", PLAYER_FRAME_COUNT, DIRECTIONS)
        
        # Set the initial texture.
        self.texture = self.idle_textures[self.direction][self.cur_texture]
        
        # The sword animation cycle in order to isolate the sword
        # textures to not combine them with the cycle of idle and walking.
        self.sword_animation_cycle = cycle([0, 1, 2, 3, 4, 5])
        
    def update_animation(self, delta_time: float = 1 / 60):
        '''
        This function is dedicated to updating animations in the code
        This is passed through on_update() to update every frame
        '''

        
        # The animation timer is += delta time to act as a timer
        # for greater control over the animation speed.
        self.animation_timer += delta_time
        
        # This conditiion checks if the player has the sword,
        # and can also swing the sword.
        if self.game.sword_collected and self.game.swing:
            # Setting texture to the sword texture + direction facing.
            self.texture = self.sword_textures\
[self.direction][self.cur_texture]

            # This controls the speed at which cur_texture changes.
            if self.animation_timer >= SWORD_ANIMATION_SPEED:
                self.animation_timer -= SWORD_ANIMATION_SPEED
                self.cur_texture = next(self.sword_animation_cycle)
            if self.cur_texture == PLAYER_FRAME_COUNT - 1:
                self.game.swing = False
        
        # Checks if player is stationary or moving and sets texture
        # appropriately. 
        elif self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction]\
[self.cur_texture]
        else:
            self.texture = self.walk_textures[self.direction]\
[self.cur_texture]
            
        
        
        # Setting player direction based on change_x and change_y.
        # Player direction saves based on the last direction.
        if self.change_x < 0:
            self.direction = 'left'
        elif self.change_x > 0:
            self.direction = 'right'
        if self.change_y > 0:
            self.direction = 'up'
        elif self.change_y < 0:
            self.direction = 'down'
        
        # This controls the speed at which cur_texture changes 
        # however with a different speed for the sword.  

        if self.animation_timer >= ANIMATION_SPEED:
            self.animation_timer -= ANIMATION_SPEED
            self.cur_texture += 1
            if self.cur_texture > PLAYER_FRAME_COUNT - 1:
                self.cur_texture = 0


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
        If the code is clicked, then this will close the 
        MainMenu window, then run the actual arcade
        window with the game in it
        '''
        # Getting the current arcade window.
        window = arcade.get_window()
        
        # This is setting the GameView (the actual game) to 
        # a view of the GameView class.
        game_view = GameView()
        
        # This shows the load screen
        # Game_view.setup() just runs the setup of the GameView() .
        game_view.setup()
        
        # And then this window just changes the view to the actual game. 
        window.show_view(game_view)
        
class MainMenu(arcade.View):
    """This method holds the main menu of the game"""

    def __init__(self):
        ''' This is the constructor for the Main Menu class. '''
        
        # Setup parent class.
        super().__init__()
        
        # Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # Label options for the title of the game on MainMenu
        # This sets the properties of the label.
        self.label = arcade.Text(
            SCREEN_TITLE,
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-200,
            arcade.csscolor.WHITE,
            70,
            anchor_x="center",
            font_name=("Kenney Pixel Square"),
        )
        
        # Label options for the instructions on MainMenu
        # This sets the properties of the label.
        self.instructions = arcade.Text(
            'To play, WASD or Arrow Keys to move. E is to swing your sword',
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-260,
            arcade.csscolor.WHITE,
            20,
            anchor_x="center",
            font_name=("Arial"),
        )
        
        # Set background color.
        arcade.set_background_color(arcade.color.BLAST_OFF_BRONZE)

        # Create a vertical BoxGroup to align buttons.
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the start button.
        start_button = StartButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Creating the quit button.
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget,
        # that will center the buttons.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        ''' This draws the Main Menu window, alongside all the 
        buttons. '''
        
        # Clears the current screen
        self.clear()
        
        # Draws the manager, labels and the instruction text.
        self.manager.draw()
        self.label.draw()
        self.instructions.draw()

class EndMenu(arcade.View):
    ''' This method containms the end menu window code'''
    def __init__(self, time_completed = 0):
        ''' This is the constructor for the End Menu class. '''
        
        # Setup parent class
        super().__init__()
        
        # Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # Setting the backgrond colour of the end menu. 
        arcade.set_background_color(arcade.color.DARK_GREEN)
        
        # Create a vertical BoxGroup to align buttons.
        self.v_box = arcade.gui.UIBoxLayout()
        
        # Creating the properties of the finish text.
        self.finish_text = arcade.Text(
            f'You finished the game! Well done!',
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT - 150,
            arcade.csscolor.WHITE,
            18,
            anchor_x= "center",
            
        )
        
        # Create the quit button
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        
        # Create a widget to hold the v_box widget,
        # that will center the buttons.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child = self.v_box)
        )
    
    def on_draw(self):
        ''' This draws the End Menu window, alongside all the 
        buttons. '''
        
        # Clears the current screen.
        self.clear()
        
        # Draws the manager, labels and the instruction text.
        self.manager.draw()
        self.finish_text.draw()

class GameView(arcade.View):
    """
    This is the main class for the actual game. This holds all the 
    code that runs the actual game. 
    """

    def __init__(self):
        ''' This is the constructor for the GameView class. '''
        
        # Call the parent class and set up the window.
        super().__init__()

        # Our Scene Object
        self.scene = None

        # Checking if the player is able to shoot.
        self.can_shoot = False
        
        # Separate variable that holds the player sprite.
        self.player_sprite = PlayerCharacter(self)
        self.enemy_sprite = EnemyCharacter()
        
        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen.
        self.camera = None
        self.gui_camera = None

        # Enemy attack damage.
        self.enemy_attack = ENEMY_ATTACK

        # Enemy condition booleans.
        self.enemy_follow = True
        self.enemy_can_attack = False
        
        # Player invincibility booleans.
        self.player_invincible = None
        self.player_invincible_time = 0
        
        # Player knockback booleans.
        self.player_knockback = None
        self.knockback_time = 0
        self.enemy_knockback = False
        
        # If the player has entered the portal boolean. 
        self.portal_enter = None
        
        # Used to check if the shoot key has been pressed.
        self.shoot_pressed = False
       
        # Stores the direction the player is facing. 
        self.player_direction = None
        
        # Stores the player's shield level.
        self.player_shield = 0
        
        # Used to specify the portal spawn point.
        self.portal_spawn_x = 0
        self.portal_spawn_y = 0
        
        # Stores information if the sword has been collected.
        self.sword_collected = False
        
        # Sets the initial level to level 1.
        self.level = LEVEL_1
        
        # Stores information if the enemy should spawn or not.
        self.enemy_spawn = None
        
        # Stores the number of orbs collected.
        self.orbs_collected = 0
        
        # Stores if the level has been complete or not.
        self.level_complete = None
        
        # Stores if the player can shoot or not.
        self.shoot_available = None

        # Stores if the enemy has died or not.
        self.enemy_dead = False
        
        # Stores the keypresses from the user.
        self.up_pressed = None
        self.down_pressed = None
        self.left_pressed = None
        self.right_pressed = None
        # This is if the user has pressed the swing key.   
        self.swing = False
        
        # Loading all the sounds required in the game.
        self.shoot_sound = arcade.load_sound("assets/shoot.mp3")
        self.hit_sound = arcade.load_sound("assets/hurt.mp3")
        self.heal_sound = arcade.load_sound("assets/heal.mp3")
        self.yay_sound = arcade.load_sound("assets/yay.mp3")

        
        # These text labels are used to display the player's 
        # health and also shield, alongisde the enemy health and quest.
        self.player_health_text = arcade.Text(
            '',
            SCREEN_WIDTH-140,
            SCREEN_HEIGHT-30,
            arcade.csscolor.BLACK,
            18,
            font_name=("Kenney Mini Square"),
            
        )
        
        self.player_shield_text = arcade.Text(
            '',
            SCREEN_WIDTH-135,
            SCREEN_HEIGHT-50,
            arcade.csscolor.BLACK,
            18,
            font_name=("Kenney Mini Square"),
            
        )
        
        self.enemy_health_text = arcade.Text(
            '',
            SCREEN_WIDTH-225,
            SCREEN_HEIGHT-70,
            arcade.csscolor.WHITE,
            18,
            font_name=("Kenney Mini Square"),
        )
        
        self.quest_text = arcade.Text(
            '',
            10,
            SCREEN_HEIGHT - 30,
            arcade.csscolor.BLACK,
            18,
            font_name=("Kenney Mini Square"),
        )
        
        
        
        # Setting the background color of the game to match 
        # the background color of the game.
        arcade.set_background_color((234, 165, 108))


############################### COMMENT FROM HERE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        
        if self.level == LEVEL_3:
            self.enemy_spawn = True
            self.enemy_can_attack = True
            
        else:
            self.enemy_spawn = False
            self.enemy_can_attack = False
        
        
        self.swing = False
        
        # Set up the Camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
                  
        
        # Layer specific options are defined based on Layer names 
        # in a dictionary
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

        # Name of map file to load
        map_name = f"maps/level_{self.level}.tmx"  
        
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap\
(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically
        # add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        
        self.player_sprite = PlayerCharacter(self)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_SLASHS)
            
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        
        
        
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
        

        # Making sure level not complte
        self.level_complete = False

        self.portal_sprite = None
        
        self.portal_enter = False
        #so slashs have a home
        #self.slash_list = arcade.SpriteList(use_spatial_hash=True)
        
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
        
        self.player_health_text.draw()
        self.player_shield_text.draw()
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
        screen_center_x = self.player_sprite.center_x - \
(self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - \
(self.camera.viewport_height/2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        
        if screen_center_y < 0:
            screen_center_y = 0
            
        if screen_center_x >= SCREEN_WIDTH:
            screen_center_x = SCREEN_WIDTH
        if screen_center_y >= SCREEN_HEIGHT:
            screen_center_y = SCREEN_HEIGHT

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
        
        pot_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_HEALTH_POT]
        )

        # Loop through each health pot we hit (if any) and remove it
        for pot in pot_hit_list:
            pot.remove_from_sprite_lists()
            self.player_shield += HEALTH_POT_VALUE
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
            if self.level == LEVEL_2:
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
            #Using trig to find the angle difference 
            # between the player and enemy
            angle = math.atan2(dist_y, dist_x)
            
            #Checks for collision between the player and enemy
            if self.player_invincible != True:
                enemy_collision = \
arcade.check_for_collision(self.player_sprite, self.enemy_sprite)
            else:
                enemy_collision = False

            #Making the enemy follow the player precicely using trig
            if self.enemy_follow == True:
                self.enemy_sprite.change_x = math.cos(angle)\
* ENEMY_MOVEMENT_SPEED
                self.enemy_sprite.change_y = math.sin(angle)\
* ENEMY_MOVEMENT_SPEED
            #Stops the enemy if there is collision
            elif self.enemy_follow == False:
                self.enemy_sprite.change_x = 0
                self.enemy_sprite.change_y = 0
                
            #Creates player knockback if enemy collides with the player
            if enemy_collision == True:
                
                if self.player_shield <= 0:
                    self.player_sprite.health -= self.enemy_attack
                else:
                    self.player_shield -= self.enemy_attack
                
                    
                self.knockback_time = 0
                self.player_knockback = True
                self.player_invincible = True
            
            #Sets how far the knockback is going to be
            if self.player_knockback == True:
                if self.knockback_time < MAX_KNOCKBACK_TIME:
                    self.player_sprite.center_x += math.cos(angle)\
* PLAYER_KNOCKBACK_SPEED
                    self.player_sprite.center_y += math.sin(angle)\
* PLAYER_KNOCKBACK_SPEED
                    self.enemy_sprite.change_x -= math.sin(angle)\
* ENEMY_KNOCKBACK_SPEED
                    self.enemy_sprite.change_y -= math.sin(angle)\
* ENEMY_KNOCKBACK_SPEED
                    
                    self.knockback_time += 1
                if self.knockback_time == MAX_KNOCKBACK_TIME:
                    self.player_knockback = False
    
        #Sets how long the invincible period is
        if self.player_invincible == True:
            if self.player_invincible_time < MAX_INVINCIBLE_TIME:
                self.player_invincible = True
                self.player_invincible_time += 1
            if self.player_invincible_time == MAX_INVINCIBLE_TIME:
                self.player_invincible = False
                self.player_invincible_time = 0
    
    
        if self.shoot_available == True:
            if self.can_shoot:
                if self.shoot_pressed:
                    print("self.swing is set to true now")
                    self.swing = True
                    arcade.play_sound(self.shoot_sound)
                    
                    slash = arcade.Sprite(f"assets/slash_sprites/slash_\
{self.player_sprite.direction}.png", SLASH_SCALING,) 
                    self.scene.add_sprite(LAYER_NAME_SLASHS, slash)
                    slash.center_x = self.player_sprite.center_x
                    slash.center_y = self.player_sprite.center_y

                    
                    if self.player_sprite.direction == 'left':
                        slash.change_x = -SLASH_SPEED
                    elif self.player_sprite.direction == 'right':
                        slash.change_x = SLASH_SPEED
                    if self.player_sprite.direction == 'up':
                        slash.change_y = SLASH_SPEED
                    elif self.player_sprite.direction == 'down':
                        slash.change_y = -SLASH_SPEED


                    #self.scene.add_sprite(LAYER_NAME_SLASHS, slash)

                    self.can_shoot = False
                
            else:
                self.shoot_timer += 1
                if self.shoot_timer == SHOOT_COOLDOWN:
                    self.can_shoot = True
                    self.shoot_timer = 0
        else:
            #print("not able to shoot dont have sword")
            pass
        
        if self.player_sprite.health <= 0:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.enemy_sprite.center_x = ENEMY_START_X
            self.enemy_sprite.center_y = ENEMY_START_Y
            self.player_sprite.health = PLAYER_HEALTH
            self.enemy_sprite.health = 100
            
        
        # Update the slash sprites
        
        for slash in self.scene[LAYER_NAME_SLASHS]:
            '''This should change to colission 
            with lists when you add more '''
            if self.level == LEVEL_3:
                hit_list = arcade.check_for_collision_with_lists(
                    slash,
                    [
                        self.scene[LAYER_NAME_ENEMIES]
                    ],
                )
            
                if hit_list:
                    for collision in hit_list:
                        if self.enemy_sprite == collision:
                            self.enemy_knockback = True
                            self.enemy_sprite.health -= SLASH_DAMAGE
                            arcade.play_sound(self.hit_sound)
                            if self.enemy_sprite.health <= 0:
                                collision.remove_from_sprite_lists()
                                self.enemy_can_attack = False
                                arcade.play_sound(self.yay_sound)
                                self.enemy_dead = True
                                self.level_complete = True

                            
                        else:
                            print("Meow")
                            
                            

                    slash.remove_from_sprite_lists()
            else:
                pass
            slash.update()
             
        
        for slash in self.scene[LAYER_NAME_SLASHS]:
            slash.update()
        
        if self.level == LEVEL_1:
            self.level_quest = f"Find all {MAX_ORBS} orbs, to open \
the portal\nOrbs collected: {self.orbs_collected}"
        elif self.level == LEVEL_2:
            self.level_quest = "Find a weapon, you'll need it..."
        elif self.level == LEVEL_3:
            self.level_quest = "You've angered the ghosts. Brace yourself."
        else:
            self.level_quest = "ERROR"
        
        
    
        self.player_health_text.text = f"Health: {self.player_sprite.health}"
        self.player_shield_text.text = f"shield: {self.player_shield}"
        if self.level == LEVEL_3:
            self.enemy_health_text.text = f"Enemy Health: {self.enemy_sprite.health}"
        self.quest_text.text = f"Quest: {self.level_quest}"
        if self.level != LEVEL_1:
            self.player_health_text.color = arcade.color.WHITE
            self.player_shield_text.color = arcade.color.WHITE
            self.quest_text.color = arcade.color.WHITE
            
        
        
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
                if self.level == LEVEL_1:
                    self.portal_spawn_x = PORTAL_SPAWN_X_L1
                    self.portal_spawn_y = PORTAL_SPAWN_Y_L1
                elif self.level == LEVEL_2:
                    self.portal_spawn_x = PORTAL_SPAWN_X_L2
                    self.portal_spawn_y = PORTAL_SPAWN_Y_L2
                elif self.level == LEVEL_3:
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
        
        if self.orbs_collected == MAX_ORBS and self.level == LEVEL_1:
            self.level_complete = True
        
        if self.portal_enter == True:
            if self.enemy_dead == True:
                # add the window here
                end_view = EndMenu()
                self.window.show_view(end_view)
                
            else:   
                self.level += 1
                self.setup()
                self.portal_enter = False
                print(self.level_complete)

        
            
                
            
            
def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH,
                           SCREEN_HEIGHT,
                           SCREEN_TITLE,
                           center_window = True)
    window.show_view(MainMenu())
    arcade.run()


if __name__ == "__main__":
    main()