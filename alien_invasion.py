# import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard
from alien import Alien


def run_game():
    # # 初始化游戏并创建一个屏幕对象
    # pygame.init()
    # screen = pygame.display.set_mode((1200, 800))  # (1200, 800) 是一个元组
    # pygame.display.set_caption("Alien Invasion")

    # 初始化 pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一个 Play 按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 创建一个用于存储游戏统计信息的实例 , 并创建记分牌
    stats = Gamestats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # # pygame 创建窗口默认是黑色的  不过可以更改颜色  且颜色是以 RGB 指定的
    # bg_color = (230, 230, 230)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个外星人
    # alien = Alien(ai_settings, screen)
    aliens = Group()

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:

            # 根据移动标志调整飞船的位置
            ship.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            #
            # # 删除已消失的子弹   因为子弹只是无法在屏幕外显示  当数量越来越多 就会占用内存 从而运行会越来越慢
            # for bullet in bullets.copy():
            #     if bullet.rect.bottom <= 0:
            #         bullets.remove(bullet)
            # # print(len(bullets))

            # 更新子弹位置，并删除已消失的子弹
            # gf.update_bullets(bullets)

            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

            # # 每次循环时都重新绘制屏幕
            # screen.fill(ai_settings.bg_color)  # 用背景色填充屏幕  screen.fill 只接受一个实参：一种颜色
            # ship.blitme()
            #
            # # 让最近绘制的屏幕可见
            # pygame.display.flip()

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
