import pygame
from .office import Office
from .clock import Clock
from .systems import *
from .power import PowerManager
from .buttons import Flick, Button
from gameplay.office import Office
from gameplay.systems import Cameras
from gameplay.power import PowerManager
from gameplay.buttons import *
from gameplay import Bonnie, Chica
from data.game.constants import *


class Game:
    def __init__(self):
        self.utils = {}
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 55)
        self.BIGGER_GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 65)
        self.office = Office()
        self.animatronics = [Bonnie(self, 10), Chica(self, 10)]
        self.events = self.init_events()
        self.flick = self.init_flick()
        self.power_manager = PowerManager()
        self.clock = Clock()
        self.debugger = True
        self._win = False
        self._killed = False

    @staticmethod
    def init_events() -> dict:
        camera_up_event = pygame.event.Event(CAMERA_FLIPPED_UP)
        camera_down_event = pygame.event.Event(CAMERA_FLIPPED_DOWN)
        return {"camera_up_event": camera_up_event, "camera_down_event": camera_down_event}

    def init_flick(self):
        screen = pygame.display.get_surface()
        flick_button = pygame.image.load('resources/ui/buttons/camera_flick.png').convert_alpha()
        camera_flick = Flick(flick_button,
                             (int(screen.get_width()/2), screen.get_height() - 25),
                             self.events['camera_up_event'],
                             self.events['camera_down_event'],
                             draw_type='midbottom',
                             scale=screen.get_width()/(screen.get_width()*1.2))
        return camera_flick

    def start(self):
        pygame.time.set_timer(UPDATE_POWER, 100)
        pygame.time.set_timer(CLOCK, 1000)
        for animatronic in self.animatronics:
            animatronic.start()

    def get_power_usage(self) -> int:
        power_usage = 1
        power_usage += self.office.get_power_usage()
        for system in self.systems.values():
            if system.active:
                power_usage += 2
        return min(power_usage, 5)

    def tick(self, event: pygame.event.Event):
        if event.type == UPDATE_POWER:
            self.power_manager.update_power(self.get_power_usage())

    def resize(self):
        screen = pygame.display.get_surface()
        for i in self.buttons:
            i.resize((int(screen.get_width()/2), screen.get_height() - 25), screen.get_width()/(screen.get_width()*2))

    def blackout(self):
        self.office.image = pygame.image.load('resources/backgrounds/office_blackout.png').convert()
        self.office.image = pygame.transform.scale_by(self.office.image, self.office.IMAGE_SCALE_SIZE)
        self.systems['Cameras'].activate_blackout()

    def win(self):
        pass # add code here for when you WIN :3

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.WINDOWRESIZED:
                for system in self.systems.values():
                    system.resize()
                self.power_manager.resize()
                self.resize()
            if event.type == BLACKOUT:
                self.blackout()
            if event.type == WIN:
                self.win()
            for animatronic in self.animatronics:
                animatronic.tick(event)
            for system in self.systems.values():
                system.tick(event)
            if not self.systems['Cameras'].blackout:
                self.flick.tick(event)
            self.office.tick(event)
            self.tick(event)
            self.clock.tick(event)
        self.office.frame()

    def global_draw(self):
        screen = pygame.display.get_surface()
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        for animatronic in self.animatronics:
            animatronic.draw()
        if not self.systems['Cameras'].blackout:
            self.flick.draw(screen)
        for button in self.buttons:
            button.draw(screen)
        self.power_manager.draw(screen)
        self.clock.draw(screen)

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass
