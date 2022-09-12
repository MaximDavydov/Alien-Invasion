class Settings():
    """Class for storage all settings game Alien Invasion."""

    def __init__(self):
        """Initialize game settings."""
        #Params of screen
        self.screen_width = 1254
        self.screen_height = 600
        # self.bg_color = (227, 49, 123)
        self.bg_color = (73, 99, 144)

        #Ship settings
        self.ship_speed = 10
        self.ship_limit = 3

        #Bullet params
        self.bullet_speed = 5
        #horizontal
        # self.bullet_width = 20
        # self.bullet_hight = 8
        self.bullet_width = 300
        self.bullet_hight = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 1000

        #Aliens settings
        self.alien_speed = 3.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #  alien_frequency controls how often a new alien appear.s
        #    Higher values -> more frequent aliens. Max = 1.0.
        self.alien_frequency = 0.008

