import sys, logging, os, random, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


SCREEN_WIDTH = 1920
SCREEN_HEIGHT= 1080
SCREEN_TITLE= "SPACE SHOOTER"

SHIP_HP= 100

NUM_ENEMIES = 5



class Player(arcade.Sprite):
    def __init__(self, image, scale, x , y):
        super.__init__(image, scale)
        self.center_x = x
        self.center_y = y
        self.dx = 0 
        self.dy = 0
        self.target_x = x
        self.target_y = y

class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__ (width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.set_mouse_visible(True)

        arcade.set_background_color(open_color.blue_4)

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list= arcade.SpriteList()


    def setup(self):
        self.playing = True
        self.score = 0.0
        self.hp = SHIP_HP    

    def update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        pass   

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


#if we are running this from the command line, run main
if __name__ == '__main__':
	main()