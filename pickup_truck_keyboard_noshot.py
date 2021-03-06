"""This is the fifth phase where the all sprites involved are introduced
with collision mechanism and moving background, plus with the keyboard handling for the vehicle."""
import pygame,random
pygame.init()

screen=pygame.display.set_mode((640,480))


class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("./assets/road2.gif")
        self.rect=self.image.get_rect()
        self.dx=5
        self.reset()

    def update(self):
        self.rect.right+=self.dx
        if self.rect.right>=1600:
            self.reset()

    def reset(self):
        self.rect.left=-1020

    

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("car2.gif")
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        self.posx=520
        self.posy=30

        if not pygame.mixer:
            print ("cannot play sound")
        else:
            pygame.mixer.init()
            self.sndgot=pygame.mixer.Sound("sndgot.ogg")
            self.sndeng=pygame.mixer.Sound("carsnd.ogg")
            self.sndcrash=pygame.mixer.Sound("sndcrash.ogg")
            self.sndeng.play(-1)

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.posy-=5
        if keys[pygame.K_DOWN]:
            self.posy+=5
        if keys[pygame.K_LEFT]:
            self.posx-=2
        if keys[pygame.K_RIGHT]:
            self.posx+=2
        if keys[pygame.K_SPACE]:
            Shot.reset(self.posx,self.posy)
        self.rect.center=(self.posx,self.posy)

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("shot.gif")
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        self.dx=10
        self.posx=20
        self.posy=20
        

    def update(self):
        #keys=pygame.key.get_pressed()
        self.rect.left-=self.dx
        #if keys[pygame.K_SPACE]:
            #Shot.reset(self,car.posx,car.posy)

    def reset(self,posx,posy):
        self.rect.centerx=posx
        self.rect.centery=posy
        self.dx=10

class Block1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pickup1.gif")
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left >screen.get_width():
            self.reset()

    def reset(self):
        self.rect.left=0
        self.rect.centerx=0
        self.rect.centery=random.randrange(0,screen.get_height())
        self.dx=5

class Block2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pickup2.gif")
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left >screen.get_width():
            self.reset()

    def reset(self):
        self.rect.left=0
        self.rect.centerx=0
        self.rect.centery=random.randrange(0,screen.get_height())
        self.dx=5

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("tree1.gif")
        self.image=self.image.convert()
        self.rect=self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left>screen.get_width():
            self.reset()

    def reset(self):
        self.rect.left=0
        self.rect.centerx=0
        self.rect.centery=random.randrange(0,screen.get_height())
        self.dx=5
        
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score=0
        self.lives=5
        self.font=pygame.font.SysFont("arial",30)

    def update(self):
        self.text="Blocks:%d Lives:%d"%(self.score, self.lives)
        self.image=self.font.render(self.text,1,(255,0,0))
        self.rect=self.image.get_rect()


        

def play():
    background=pygame.Surface(screen.get_size())
    screen.blit(background,(0,0))
    car=Car()
    shot=Shot()
    block1=Block1()
    block2=Block2()
    tree=Tree()
    road=Road()
    scoreboard=Scoreboard()
    allSprites=pygame.sprite.Group(road,block1,block2,tree,car,shot)
    scoresprite=pygame.sprite.Group(scoreboard)
        
    clock=pygame.time.Clock()
    loop=True
    while loop:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False

        if car.rect.colliderect(block1.rect):
            car.sndgot.play()
            block1.reset()
            scoreboard.score+=1
        if car.rect.colliderect(block2.rect):
            car.sndgot.play()
            block2.reset()
            scoreboard.score+=1
            if scoreboard.score>50:
                scoreboard.lives+=1
                scoreboard.score=0
				
        if car.rect.colliderect(tree.rect):
            car.sndcrash.play()
            tree.reset()
            scoreboard.lives-=1
            scoreboard.score=0
	    
            if scoreboard.lives<0:
                loop=False
      #  if shot.rect.colliderect(tree.rect):
       #     tree.reset()
            
        allSprites.update()
        scoresprite.update()
        
        allSprites.draw(screen)
        scoresprite.draw(screen)
        
        pygame.display.flip()
        #pygame.mouse.set_visible(True)
    return scoreboard.score

def instructions(score):
    pygame.display.set_caption("!@#Get Blocks@!")
    car=Car()
    road=Road()
    showSprite=pygame.sprite.Group(car,road)
    insFont=pygame.font.SysFont(None,25)
    insLabels=[]
    instructions=(
        "Get Blocks. Your score:%d"%score,
        "You need to collect all the jewels and money bags",
        " by sliding over them. If you hit a tree your lives",
        " will decrease.Collect as many ornaments as you can.",
        "Get a life bonus for exchange of 50 points",
        " You may click to start the game,Press esc if you are chicken",
        "Use the keyboard navigation keys to navigate"
        )
    for line in instructions:
        tempLabel=insFont.render(line,1,(0,250,10))
        insLabels.append(tempLabel)
    loop=True
    clock=pygame.time.Clock()
    #pygame.mouse.set_visible(False)
    while loop:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
                finish=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                loop=False
                finish=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    loop=False
                    finish=True

        showSprite.update()
        showSprite.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i],(50,30*i))

        pygame.display.flip()
    #pygame.mouse.set_visible=(True)
    #car.sndeng.stop()
    return finish
	
def main():
    finish=False
    score=0
    while not finish:
        finish=instructions(score)
        if not finish:
            score=play()

                    
    
        
if __name__=="__main__":
    main()

        
