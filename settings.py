class Settings():
    """Class for storage all settings game Alien Invasion."""

    def __init__(self):
        """Initialize game settings."""
        #Params of screen
        self.screen_width = 1200
        self.screen_height = 600
        # self.bg_color = (227, 49, 123)
        self.bg_color = (73, 99, 144)

        #Ship settings
        self.ship_speed = 10

        #Bullet params
        self.bullet_speed = 5
        #horizontal
        # self.bullet_width = 20
        # self.bullet_hight = 8
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 1000

