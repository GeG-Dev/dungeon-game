import pygame
font = pygame.font.SysFont("Arial" , 22)

class button:
    def __init__(self , xPos , yPos , width , height , color , hoverColor , text , radius = 10):
        self.rect = pygame.Rect(xPos , yPos , width , height)
        
        self.mainColor = color
        self.hoverColor = hoverColor
        self.currentColor = self.mainColor
        self.radius = radius
        
        self.text = font.render(text , True , (255,255,255))
        self.textRect = self.text.get_rect(center=self.rect.center)
    
    def draw(self , screen):
        pygame.draw.rect(screen, self.currentColor,self.rect ,border_radius=self.radius )
        screen.blit(self.text , self.textRect)
        
    def checkHover(self , mousePos):
        if self.rect.collidepoint(mousePos):
            self.currentColor = self.hoverColor
        else:
            self.currentColor = self.mainColor
    def click(self , event , mousePos):
        if event.type == pygame.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(mousePos):
                return True
        return False