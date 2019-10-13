class Settings():
    """存储游戏的所有设置类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹设置
        # self.bullet_speed_factor = 3
        self.bullet_width = 8
        self.bullet_height = 15
        self.bullet_color = 248, 60, 0
        self.bullet_allowed = 4

        # 外星人设置
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 28
        # self.fleet_direction 为 1 表示向右移动 ，-1 表示向左移
        # self.fleet_direction = 1
        # self.fleet_direction = 1

        # 加快游戏节奏的速度
        self.speedup_scale = 1.0

        # 外星人点数的提高速度
        self.score_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.0
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.8

        # self.fleet_direction 为 1 表示向右移动 ，-1 表示向左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 10



    def increase_speed(self):
        """提高速度设置和外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
