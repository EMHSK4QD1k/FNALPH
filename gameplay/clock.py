from data.game.constants import *


class Clock:
    def __init__(self):
        self.HOUR_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 100)
        self.NIGHT_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 50)
        self.night = None
        self.HOUR_DURATION = None
        self._time = None
        self.hour = None
        self.active = None

    def start(self, night):
        # 60 is too long. Keep this at 45
        # Change the difficulty to balance for 45
        # Right. Give me a second
        self.HOUR_DURATION = 45
        self._time = 12
        self.hour = 0
        self.active = True
        self.night = night

        pygame.time.set_timer(CLOCK, self.HOUR_DURATION * 1000)

    def stop(self):
        self.night = 0
        self.hour = 0
        self._time = 12
        pygame.time.set_timer(CLOCK, 0)

    def tick(self, event: pygame.event.Event):
        if event.type == CLOCK:
            self.update_time()

    def draw(self, screen: pygame.Surface):
        width = screen.get_width()
        render = self.HOUR_FONT.render(f"{self.time} AM", True, 'white')
        rect = render.get_rect()
        rect.topright = (width - 20, 20)
        screen.blit(render, rect)
        night = self.NIGHT_FONT.render(f"Night {self.night}", True, 'white')
        night_rect = night.get_rect()
        night_rect.topright = (width - 20, rect.height - 10)
        screen.blit(night, night_rect)

    def update_time(self):
        if self.active:
            self.hour += 1
            self.time = int((self.hour - 1) % 12 + 1)
            if self._time == 6:
                pygame.event.post(pygame.event.Event(WIN))
                self.active = False
