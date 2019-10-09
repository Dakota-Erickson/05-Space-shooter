import sys, logging, os, random, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


SCREEN_WIDTH = 1920
SCREEN_HEIGHT= 1080
MARGIN = 50
SCREEN_TITLE= "SPACE SHOOTER"

SHIP_HP= 100
SHIP_SCALE= .5
SHIP_MAX_Y = SCREEN_HEIGHT // 3

BULLET_SCALE = 1
BULLET_SPEED = 10
BULLET_DAMAGE = 2

SCORE_DECREASE = .1

NUM_ENEMIES = 5
ENEMY_SCALE = .5
ENEMY_MIN_Y = 400
ENEMY_MIN_HP = 5
ENEMY_MAX_HP = 10
ENEMY_MIN_MASS = 10
ENEMY_MAX_MASS = 100
ENEMY_ACCELERATION = 10
ENEMY_MAX_ACCELERATION = 3
ENEMY_PROB_SHOOT = .05
ENEMY_PROB_CHANGE_POS = .05

ENEMY_BULLET_DAMAGE = 10
ENEMY_BULLET_SPEED = -4

sign = lambda x: x and (1, -1)[x < 0]



class Player(arcade.Sprite):
    def __init__(self, image, scale, x , y):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.dx = 0 
        self.dy = 0
        self.target_x = x
        self.target_y = y

    def update_target(self, x, y,):
        self.target_x = min(max(MARGIN, x), SCREEN_WIDTH - MARGIN)
        self.target_y = min(max(MARGIN, y), SHIP_MAX_Y)  

    def update(self):
        if self.center_x != self.target_x:
            self.center_x = self.target_x
        if self.center_y != self.target_y:
            self.center_y = self.target_y  
        if self.center_x <= MARGIN:
            self.center_x = MARGIN
        if self.center_x >= SCREEN_WIDTH - MARGIN:
            self.center_x = SCREEN_WIDTH - MARGIN
        if self.center_y <= MARGIN:
            self.center_y = MARGIN               



class Enemy(arcade.Sprite):
    def __init__(self, x, y, mass, hp):
        sprites = ['Enemy_Red', 'Enemy_Yellow']
        sprite = random.choice(sprites)
        super().__init__("assets/{}.png".format(sprite), ENEMY_SCALE)
        self.center_x = x
        self.center_y = y
        self.hp = hp
        self.mass = mass
        self.dx = 0 
        self.dy = 0
        self.target_x = x
        self.target_y = y    
        self.acceleration = ENEMY_ACCELERATION / self.mass    

    def update_target(self, x, y,):
        self.target_x = min(max(MARGIN, x), SCREEN_WIDTH - MARGIN)
        self.target_y = min(max(ENEMY_MIN_Y, y), SCREEN_HEIGHT - MARGIN)  


    def update(self):
        if self.center_x != self.target_x:
            self.dx += self.acceleration * sign(self.target_x - self.center_x)
            self.dx = min(self.dx, ENEMY_MAX_ACCELERATION)
            self.center_x += self.dx
        if self.center_y != self.target_y:
            self.dy += self.acceleration * sign(self.target_y - self.center_y)
            self.dy = min(self.dy, ENEMY_MAX_ACCELERATION)
            self.center_y += self.dy
        if self.center_x <= MARGIN:
            self.center_x = MARGIN
            self.dx = abs(self.dx)
        if self.center_x >= SCREEN_WIDTH - MARGIN:
            self.center_x = SCREEN_WIDTH - MARGIN
            self.dx = abs(self.dx) * -1
        if self.center_y <= MARGIN:
            self.center_y = MARGIN
            self.dy = abs(self.dy)*-1 

class Bullet(arcade.Sprite):
    def __init__ (self, image, scale, x ,y , dx, dy, damage):
        super().__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy    

class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__ (width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.set_mouse_visible(True)

        self.background = None

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list= arcade.SpriteList()


    def setup(self):
        self.playing = True
        self.score = 0.0
        self.hp = SHIP_HP    
        self.background = arcade.load_texture("assets/background.png")
        self.score = 1000

        self.player = Player("assets/Player_Blue.png", SHIP_SCALE, SCREEN_WIDTH // 2, 100)
        self.player_list.append(self.player)

        for e in range(NUM_ENEMIES):
            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = random.randint(SCREEN_HEIGHT-ENEMY_MIN_Y,SCREEN_HEIGHT-MARGIN)
            hp = random.randint(ENEMY_MIN_HP,ENEMY_MAX_HP)
            mass=random.randint(ENEMY_MIN_MASS,ENEMY_MAX_MASS)
            enemy = Enemy(x, y, mass, hp)
            self.enemy_list.append(enemy)

    def update(self, delta_time):
        if self.playing:
            self.player_list.update()
            self.enemy_list.update()
            self.bullet_list.update()
            self.enemy_bullet_list.update()

            self.score -= SCORE_DECREASE

            for e in self.enemy_list:
                if random.random() < ENEMY_PROB_SHOOT:
                    self.shoot_enemy_bullet(e)

                if random.random() < ENEMY_PROB_CHANGE_POS:
                    x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
                    y = random.randint(SCREEN_HEIGHT-ENEMY_MIN_Y,SCREEN_HEIGHT-MARGIN)
                    e.update_target(x,y)    

                bullets = arcade.check_for_collision_with_list(e, self.bullet_list)
                for b in bullets:
                    e.hp -= b.damage
                    b.kill()
                    self.score += 10
                if e.hp <= 0:
                    e.kill()   
                    self.score += 100
        enemy_bullets = arcade.check_for_collision_with_list(self.player, self.enemy_bullet_list)
        for eb in enemy_bullets:
            self.hp -= eb.damage
            eb.kill()
            self.score -= 10
        if  self.hp<=0:
            self.hp = 0     
            self.playing = False           



    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

        arcade.draw_text("Score: {}".format(int(self.score)), 10, SCREEN_HEIGHT - 30, open_color.white, 16)
        arcade.draw_text("HP: {}".format(int(self.hp)), SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30, open_color.white, 16)
        arcade.draw_text(self.title, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, open_color.white, 16)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.player.update_target (x,y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.shoot_bullet()

    def shoot_bullet(self):
        image = "assets/Blue_Laser.png"
        x= self.player.center_x
        y = self.player.center_y + (self.player.height // 2)
        dy = BULLET_SPEED
        bullet = Bullet(image, BULLET_SCALE, x, y, 0, dy, BULLET_DAMAGE)
        self.bullet_list.append(bullet)        

    def shoot_enemy_bullet(self, enemy):
        image = "assets/Red_Laser.png"
        x= enemy.center_x
        y = enemy.center_y - (self.player.height // 2)
        dy = ENEMY_BULLET_SPEED
        bullet = Bullet(image, BULLET_SCALE, x, y, 0, dy, ENEMY_BULLET_DAMAGE)
        self.enemy_bullet_list.append(bullet)       

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


#if we are running this from the command line, run main
if __name__ == '__main__':
	main()