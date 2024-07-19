import pygame
import random 
import math
import time

#Initialize pygame
pygame.init()

#Screen
screen = pygame.display.set_mode((800,600))

#Title
pygame.display.set_caption("Space Invaders")

#Icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("background.png")

#Score variable
score = 0

# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load sound effects
collision_sound = pygame.mixer.Sound("explosion.mp3")
missile_sound = pygame.mixer.Sound("bullet.mp3")


#Setting playerImg and Coordinates
player = pygame.image.load("aircraft.png")
playerX = 360
playerY = 500
playerCHX = 0


#Setting alienImg and Coordinates
alien = pygame.image.load("alien.png")
alienX = random.randint(0,736)
alienY = random.randint(50,150)
alienCHX = 3
alienCHY = 20


#Setting missile
missile = pygame.image.load("missile.png")
missileX = 0
missileY = 500
missileCHY = -10
missile_state = "ready"



#Drawing the player image using blit
def display_player(x,y):
    screen.blit(player,(x,y))

#Drawing the alien image using blit
def display_alien(x,y):
    screen.blit(alien,(x,y))

#Initialize missile_state to fire    
def shoot(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile,(x+16,y+10))    

#Collision
def collision(alienX,alienY,missileX,missileY):
    distance = math.sqrt((math.pow((alienX-missileX),2))+(math.pow((alienY-missileY),2)))    
    if distance<25:
        return True
    else:
        return False

def collision_Alien(alienX,alienY,playerX,playerY):
    distance = math.sqrt((math.pow((playerX-alienX),2))+(math.pow((playerY-alienY),2)))    
    if distance<60:
        return True
    else:
        return False


def gameOver():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))   
    pygame.display.update()
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play(1)
    time.sleep(10)        

#Game Loop
running = True
while running:
    
    #Clear screen
    screen.fill((0, 0, 0))
    
    #Background
    screen.blit(background,(0,0))
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerCHX -= 5
            if event.key == pygame.K_RIGHT:
                playerCHX += 5   
            if event.key == pygame.K_SPACE:
                #After missile reaches the border only then fire next bullet
                if missile_state=="ready":
                    missileX = playerX
                    shoot(missileX,missileY) 
                    missile_sound.play()        
                
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerCHX = 0 
                            
    
    #Updating player movement
    playerX+=playerCHX
    
    #Setting boundary for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Updating alien movement
    alienX+=alienCHX
    
    #Setting boundary for alien
    if alienX <= 0: 
        alienCHX = 3
        alienY += alienCHY         
    elif alienX >= 736:
        alienCHX = -3
        alienY += alienCHY
    
    
    #Missile Movement
    
    #if missile reaches border reset missile_state to ready
    if missileY <= 0:
        missileY = 500
        missile_state="ready"
    
    # if missile is fire state then display missile
    if missile_state == "fire":
        missileY+=missileCHY
        shoot(missileX,missileY)
    
         
        
    iscollided = collision(alienX,alienY,missileX,missileY)    
    if iscollided:
        collision_sound.play()
        missileY=500
        missile_state="ready"
        alienX=random.randint(0,736)
        alienY=random.randint(50,150)
        score+=1
        print("Your Score:",score)
    
    iskilled = collision_Alien(alienX,alienY,playerX,playerY)    
    if iskilled:
        gameOver()
        running = False
       
    #Calling player_display
    display_player(playerX,playerY)
    
    #Calling display_alien
    display_alien(alienX,alienY)

    font = pygame.font.Font(None, 50)
    score_text = font.render("Score:"+str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    #Updating display i.e game window
    pygame.display.update()