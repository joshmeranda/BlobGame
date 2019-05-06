"""
    SqueakersAnimated.py
    4/9/2019
    Izabele Bauzyte
    
    Images and sounds made by Izabele Bauzyte

    Music:
    Monkeys Spinning Monkeys Kevin MacLeod (incompetech.com)
    Licensed under Creative Commons: By Attribution 3.0 License
    http://creativecommons.org/licenses/by/3.0/

    This game creates bunnies on screen and the player is tasked
    with capturing the bunnies to win the game.
    They are scored by the time.

"""

#import and initialize
import pygame
import random, time, SqueakerGameSprites
pygame.init()

if not pygame.mixer:
    
    print("problem with sound")
    
else:
    
    pygame.mixer.init()
    
    music = pygame.mixer.Sound("music\MonkeysSpinningMonkeys.ogg")
    music.play(-1)

screen = pygame.display.set_mode((800, 800))

def main():
    
    #display
    pygame.display.set_caption("Catch all the squeakers before they run away!")
    pygame.mouse.set_visible(False)

    #entities
        # background
    background = pygame.image.load("images\grassyBackground.png").convert()
    screen.blit(background, (0,0))

        # squeakers
    squeakList = []
    numSqueaks = 10
    
    for i in range(numSqueaks):
        squeakList.append(SqueakerGameSprites.Squeaker(screen))
    squeakGroup = pygame.sprite.Group(squeakList)

        # player sprite circle
    circle = SqueakerGameSprites.Circle()
    circleGroup = pygame.sprite.Group(circle)

        # score icons
    scoreGroup = pygame.sprite.Group()

        # sprite list
    sprites = []
    sprites.append(scoreGroup)
    sprites.append(squeakGroup)
    sprites.append(circleGroup)

    #assign
    clock = pygame.time.Clock()
    keepGoing = True
    score = 0
    start = time.time()

    #loop
    while keepGoing:

        #time
        clock.tick(30)

        #events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                keepGoing = False

        # handles collisions between mouse and squeakers
        squeaksCaught = pygame.sprite.spritecollide(circle, squeakGroup, True)
        if not squeaksCaught == []:
            
            for squeak in squeaksCaught:

                squeak.play_squeak()

                # adds an image of a captured bunny to bottom of screen
                scoreIcon = squeak.imgPath + "scoreIcon.png"
                scoreGroup.add(SqueakerGameSprites.ScoreItem((score * 70), screen.get_height() - 20, scoreIcon))
                
                score += 1

        # winning condition and output labels
        if score == numSqueaks:

            score = 0

            elapsedTime = time.time() - start

            labelGroup = pygame.sprite.Group(SqueakerGameSprites.Label("You caught them all!",
                                                    (screen.get_width() / 2,
                                                     screen.get_height() / 2),
                                                    (255, 255, 255)))

            labelGroup.add(SqueakerGameSprites.Label("It took you " + "{:.2f}".format(elapsedTime) + " seconds.",
                                (screen.get_width() / 2, (screen.get_height() / 2) + 40),
                                (255, 255, 255)))
            
            sprites.append(labelGroup)
        
        #update
        for spriteGroup in sprites:
            
            spriteGroup.clear(screen, background)
            spriteGroup.update()
            spriteGroup.draw(screen)


        #refresh
        pygame.display.flip()

    pygame.quit()
    
if __name__ == "__main__":
    main()
