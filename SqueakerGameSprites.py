"""
SqueakerGameSprites.py
Izabele Bauzyte
4/11/2019

A collection of all the sprites used for the squeaker game
"""

import pygame, random

class Squeaker(pygame.sprite.Sprite):
    """
    A bunny sprite
    """

    def __init__(self, screen):

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        # squeak sound
        self.squeakSounds = ["squeak1.ogg", "squeak2.ogg", "squeak3.ogg"]
        self.squeak = pygame.mixer.Sound("sounds\\" + random.choice(self.squeakSounds))

        # 3 pattern options
        self.possiblePatterns = ["squeaker1", "squeaker2", "squeaker3"]
        self.pattern = random.choice(self.possiblePatterns)        

        # picks which animation frame is displayed first
        self.imgPath = "images\\" + self.pattern + "\\"
        self.patternVariants = [(self.imgPath + "squeaker1.png"), (self.imgPath + "squeaker2.png")]
        self.patternVariant = random.choice(self.patternVariants)
        self.image = pygame.image.load(self.patternVariant).convert_alpha()

        # motion speed
        self.dx = random.randint(-5, 5)
        self.dy = random.randint(-5, 5)

        # adjusts image facing direction based on motion
        if self.dx < 0:
            
            self.facingRight = False
            self.image = pygame.transform.flip(self.image, True, False)
            
        else:
            
            self.facingRight = True

        # rect
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.top = random.randint(0, self.screen.get_height() - self.rect.height - 110)

        # for animation purposes
        self.animationRate = random.randint(3, 7)
        self.imgIndex = 0   # which animation in the folder the sprite currently displays
        self.frame = 0      # frame rate of animation

    def animate(self):
        """
        Toggles between the image variants for a certain bunny pattern
        """

        # is number of times through the main loop > rate of animation
        if self.frame > self.animationRate:

            # reset
            self.frame = 0

            # changes animation image and adjusts orientation
            if self.imgIndex == 0:
                
                self.image = pygame.image.load(self.patternVariants[self.imgIndex]).convert_alpha()
                self.imgIndex = 1

                if not self.facingRight:

                    self.image = pygame.transform.flip(self.image, True, False)

            else:
                
                self.image = pygame.image.load(self.patternVariants[self.imgIndex]).convert_alpha()
                self.imgIndex = 0

                if not self.facingRight:

                    self.image = pygame.transform.flip(self.image, True, False)

        # increment frame #
        else:
            
            self.frame += 1

    def checkBounds(self):
        """
        adjusts dx and dy if sprite out of bounds
        """

        # adjusts dx and dy if sprite out of bounds
        if self.rect.left < 0:

            self.facingRight = True
            self.dx *= -1
            
        elif self.rect.right > self.screen.get_width():
            
            self.facingRight = False
            self.dx *= -1
            
        elif self.rect.top < 0:
            
            self.dy *= -1
            
        elif self.rect.bottom > self.screen.get_height() - 110:
            
            self.dy *= -1
            # sprite sometimes freaks out on the bottom, this line stops it
            self.rect.centery += self.dy

        # move sprite
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

    def update(self):

        self.checkBounds()
        self.animate()

    def play_squeak(self):
        """
        sound effect
        """

        self.squeak.play()

class Circle(pygame.sprite.Sprite):
    """
    A Circle sprite that follows the user's mouse
    """

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\cageCircle.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):

        # follows mouse
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

class ScoreItem(pygame.sprite.Sprite):
    """
    A score item that appears on screen each time the
    user catches a squeaker
    """

    def __init__(self, leftLoc, bottomLoc, img):
        """
        accepts location (left and right) and the image to be displayed
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = bottomLoc
        self.rect.left = leftLoc

class Label(pygame.sprite.Sprite):
    """
    Object to display text
    """
    
    def __init__(self, text, loc, color):
        """
        Accepts text to be displayed
        location on screen (x, y)
        and the color of the text
        """

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("None", 60)
        self.text = text
        self.color = color

        # image
        self.image = self.font.render(self.text, 1, self.color)

        # loc
        self.rect = self.image.get_rect()
        self.rect.center = loc
