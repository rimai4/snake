import pygame


class Control:
    def __init__(self, size, fps):
        self.size = size
        self.fps = fps
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = state_dict[self.state_name]
        self.state.setup()

    def flip_state(self):
        self.state.done = False
        self.state.cleanup()
        self.state_name = self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.setup()

    def update(self, dt):
        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()
