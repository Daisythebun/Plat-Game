from Start_Game import SPRITE_SCALING_PLAYER
import arcade #py -m venv venv


MUSIC_VOLUME = 0.0
SPRITE_SCALING = 0.5
TILE_SCALING = 0.9

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer"


MOVEMENT_SPEED = 3
GRAVITY = .2 #change this to enable jumping
JUMP_SPEED = 11  

VIEWPORT_MARGIN = 250

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 20


class Player(arcade.Sprite):
    """ Player Class """

    def __init__(self):

        super().__init__()
        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0
        self.health = 5
        self.has_lost = False

        self.scale = SPRITE_SCALING_PLAYER

        main_path = "Sprites/mario/mario"

        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        self.walk_textures = []
        for i in range(3):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

        #Hit box is based on first image used
        self.hit_box = self.texture.hit_box_points

        #Player will default to face right
        self.character_face_direction = RIGHT_FACING

        #Index of current texture
        self.cur_texture = 0

        #distance traveled since changed texture
        self.x_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometer += dx

        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0

            self.cur_texture += 1
            if self.cur_texture > 2:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    def reset_pos(self):
        self.center_x = 100
        self.center_y = 160


    def reset(self): # reset the player
        self.reset_pos()
        self.has_lost = False
        self.reset_health = self.health = 3 # health of the player

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        #self.center_x += self.change_x
        #self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        #angle_rad = math.radians(self.angle)

        #self.angle += self.change_angle

        #self.center_x += -self.speed * math.sin(angle_rad)
        #self.center_y += -self.speed * math.cos(angle_rad)		#change
