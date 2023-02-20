import pygame


class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(
            self.size  # pyright: ignore[reportGeneralTypeIssues]
        )
        self.clock = pygame.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = state_dict[self.state_name]

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
            delta_time = (
                self.clock.tick(self.fps)  # pyright: ignore[reportGeneralTypeIssues]
                / 1000.0
            )
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()
