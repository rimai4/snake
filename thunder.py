class Thunder:
    def __init__(self, game):
        self.game = game
        thunder_image = pygame.image.load("thunder.png")
        self.image = pygame.transform.scale(thunder_image, (20, 20)).convert()

    def draw(self):
        pass
