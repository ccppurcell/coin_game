
import pygame

import random

class Object:
    #common functionality like basic movement, collision detection

    def __init__(self):
        #location
        self.x = 0
        self.y = 0

        #dimensions
        self.height = 0
        self.width = 0

        #velocity
        self.vel = 0

    def update(self):
        window.blit(self.image, (self.x, self.y))
    
    def move_up(self):
        self.y-=self.vel
    
    def move_down(self):
        self.y+=self.vel
    
    def move_left(self):
        self.x-=self.vel
    
    def move_right(self):
        self.x+=self.vel

    def loc(self, avoid:int):
        #picks a location avoiding a given quadrant (i.e. the player)

        #pick quadrant
        quadrant = avoid
        while quadrant == avoid:
            quadrant = random.randint(1,8)

        #pick coords inside quadrant
        x_init = random.random()
        y_init = random.random()

        #assign x coord
        if quadrant in [1,4,7]:
            self.x = monster_w + x_init*((field_w-self.width)/3)
        if quadrant in [2,5,8]:
            self.x = monster_w + (1+x_init)*((field_w-self.width)/3) 
        if quadrant in [3,6,9]:
            self.x = monster_w + (2+x_init)*((field_w-self.width)/3)

        #assign y coord
        if quadrant in [1,2,3]:
            self.y = monster_h + y_init*((field_h-self.height)/3)
        if quadrant in [4,5,6]:
            self.y = monster_h + (1+y_init)*((field_h-self.height)/3)
        if quadrant in [7,8,9]:
            self.y = monster_h + (2+y_init)*((field_h-self.height)/3)

    def overlaps(self, other:"Object"):
        #detect collisions

        #set margin
        margin = 10

        #collision conditions
        right_enough = self.x+self.width > other.x + margin
        left_enough = self.x < other.x + other.width - margin
        low_enough = self.y+self.height > other.y + margin
        high_enough = self.y < other.y + other.height - margin

        return right_enough and left_enough and low_enough and high_enough

class Robot(Object):
    '''The player object'''

    def __init__(self):

        #player always starts in the centre
        self.x = (width - rob_w)//2
        self.y = (height - rob_h)//2

        self.image = images["robot"]
        self.width = rob_w
        self.height = rob_h
        self.vel = 5
        self.quadrant = 5

    def move_up(self):
        #keep the player in the field
        self.y-=self.vel if self.y>monster_h else 0
        self.quadrant = self.get_quadrant()
    
    def move_down(self):
        self.y+=self.vel if self.y+self.height<height-monster_h else 0
        self.quadrant = self.get_quadrant()
    
    def move_left(self):
        self.x-=self.vel if self.x>monster_w else 0
        self.quadrant = self.get_quadrant()
    
    def move_right(self):
        self.x+=self.vel if self.x+self.width < width-monster_w else 0
        self.quadrant = self.get_quadrant()

    def get_quadrant(self):
        #gets the current quadrant:
        # 1 2 3
        # 4 5 6
        # 7 8 9

        #narrow down quadrant by x coord
        if self.x<monster_w+field_w/3:
            poss = [1,4,7]
        elif self.x<monster_w + 2 * field_w/3:
            poss = [2,5,8]
        else:
            poss = [3,6,9]

        #select quadrant by y coord
        if self.y < monster_h+field_h/3:
            return poss[0]
        elif self.y < monster_h + 2*field_h/3:
            return poss[1]
        else:
            return poss[2]
    
class Monster(Object):
    '''Enemies that move across the screen'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = images["monster"]
        self.width = monster_w
        self.height = monster_h
        self.vel=3
    
class Coin(Object):
    '''Coins for the player to collect'''

    def __init__(self):
        self.image = images["coin"]
        self.width = coin_w
        self.height = coin_h

        #player starts in quadrant 5
        self.loc(5)

class Door(Object):
    '''Reaching the door increases the level'''

    def __init__(self):
        self.x = (width-door_w)//2
        self.y = (height - door_h)//2
        self.image = images["door"]
        self.width = door_w
        self.height = door_h

#load images
images = {
    "robot" : pygame.image.load("images/robot.png"),
    "door" : pygame.image.load("images/door.png"),
    "monster" : pygame.image.load("images/monster.png"),
    "coin" : pygame.image.load("images/coin.png")
}

#get sizes
sizes = {name: img.get_size() for name, img in images.items()}

#get widths and heights
rob_w, rob_h = sizes["robot"]
door_w, door_h = sizes["door"]
monster_w, monster_h = sizes["monster"]
coin_w, coin_h = sizes["coin"]


#set dimensions
width, height = 800, 550

#border has the same dimensions as monster
border_w, border_h = monster_w, monster_h

#player is confined to field
field_w, field_h = width-border_w-border_w, height-border_h-border_h


#init window
window = pygame.display.set_mode((width,height))
background_colour = (100,100,100)
window.fill(background_colour)
pygame.display.set_caption("Collect coins, avoid monsters, open the door!")

#initialise pygame
pygame.init()

#other utilities
clock=pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 24)
small_coin = pygame.transform.scale(
        images["coin"], (coin_w//2,coin_h//2)
        )
caught_text = game_font.render("They got you! Enter to play again...", True, (255,100,255))
ct_w, ct_h = caught_text.get_width(), caught_text.get_height()

def update_header(collected:int, level:int):
    #shows the coins collected and the level
    
    if collected>0:
        #show a small coin for each coin collected, top left
        for i in range(collected):

            #calculate small coin location
            coin_x = border_w+i*coin_w//2
            coin_y = border_h//2

            #blit small coin
            window.blit(small_coin, (coin_x, coin_y))
    
    #show the current level at the top
    #render current level text
    level_text = game_font.render(f"Level {level}", True, (255,0,0))

    #calculate level text size
    lt_w = level_text.get_width()
    lt_h = level_text.get_height()

    #calculate level text position
    lt_x = (width-lt_w)//2
    lt_y = (border_h-lt_h)//2

    #blit level text
    window.blit(level_text, (lt_x, lt_y))

if __name__ == "__main__":        

    #init the player
    player = Robot()
    left = right = up = down = False
    caught = False

    #init the monsters
    north = []
    east = []
    west = []
    south = []

    #first monster appears in a fixed place when the game starts
    first_mon_x = 200
    north.append(Monster(first_mon_x,-monster_h))

    #init the targets
    the_coin=Coin()
    the_door=Door()
    door_open=False

    #init the stats
    level = 1
    collected = 0

    running=True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left=True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_DOWN:
                    down = True
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_DOWN:
                    down = False
            elif event.type==pygame.QUIT:
                running = False

        if not running:
            break

        #move the player
        if left:
            player.move_left()
        if right:
            player.move_right()
        if up:
            player.move_up()
        if down:
            player.move_down()

        difficulty = 1.4
        #add a monster coming from the north
        #rolling the dice both to decide whether to add and how far along the x axis to start
        #more monsters are added as the level gets higher
        roll_dice = random.random()*(100+400/(level*difficulty))
        if roll_dice<1:
            x_init = roll_dice*(width-monster_w)
            north.append(Monster(x_init,-monster_h))
        
        #add a monster coming from the east
        if level>1:
            roll_dice = random.random()*(100+400/(level*difficulty))
            if roll_dice<1:
                y_init = roll_dice*(height-monster_h)
                east.append(Monster(width,y_init))
        
        #add a monster coming from the south
        if level>2:
            roll_dice = random.random()*(100+400/(level*difficulty))
            if roll_dice<1:
                x_init = roll_dice*(width-monster_w)
                south.append(Monster(x_init,height))

        #add a monster coming from the west
        if level>3:
            roll_dice = random.random()*(100+400/(level*difficulty))
            if roll_dice<1:
                y_init = roll_dice*(height-monster_h)
                west.append(Monster(-monster_w,y_init))

        #create the playing field   
        window.fill((100,100,100))  

        #create north border
        pygame.draw.rect(window, (0,0,0), (0,0,width,border_h))

        #create west border
        pygame.draw.rect(window, (0,0,0), (0,0,border_w,height))

        #create east border
        pygame.draw.rect(window, (0,0,0), (width-border_w,0,border_w,height))

        #create south border
        pygame.draw.rect(window, (0,0,0), (0,height-border_h,width,border_h))
        update_header(collected,level)
            

        if player.overlaps(the_coin) and not door_open:
            #relocate the coin, avoiding the player
            the_coin.loc(player.quadrant)

            #collect a coin
            collected+=1

        #set the target number of coins
        target = level+2
        
        if collected >= target:

            if not door_open:

                the_door.loc(player.quadrant)

                door_open = True


            #show the door
            the_door.update()

            if player.overlaps(the_door):

                #increase the level
                level+=1

                #reset
                collected=0
                door_open = False

        if not door_open:
            #show the coin
            the_coin.update()

        #north monsters
        for mon in north:
            #lose condition
            if mon.overlaps(player):
                caught = True
                break
            
            #otherwise move and update the monster
            mon.move_down()
            mon.update()

        #east monsters
        if not caught:
            for mon in east:
                if mon.overlaps(player):
                    caught = True
                mon.move_left()
                mon.update()

        #south monsters
        if not caught:
            for mon in south:
                if mon.overlaps(player):
                    caught = True
                mon.move_up()
                mon.update()

        #west monsters
        if not caught:
            for mon in west:
                if mon.overlaps(player):
                    caught = True
                mon.move_right()
                mon.update()
        
        while caught:
            #display text indicating caught, what to do to play again
            window.blit(caught_text, ((width-ct_w)/2,(height-ct_h)/2))
            pygame.display.flip()

            for event in pygame.event.get():
                #make sure player can quit here
                if event.type == pygame.QUIT:
                    exit()

                #player can start again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        #reset everything
                        level = 1
                        collected = 0
                        caught = False
                        player = Robot()
                        the_coin=Coin()
                        north=[]
                        east=[]
                        south=[]
                        west=[]
                        up=right=down=left=False
                        door_open = False

        #display the player
        player.update()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
