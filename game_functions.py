import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # # 创建一个子弹，并将其加入到编组 bullets 中
        # if len(bulltes) < ai_settings.bullet_allowed:
        #     new_bullet = Bullet(ai_settings, screen, ship)
        #     bulltes.add(new_bullet)
        fire_bullet(ai_settings, screen, ship, bullets)

    # 为退出程序添加一个快捷键
    elif event.key == pygame.K_q:
        sys.exit()


def get_numbers_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    numbers_aliens_x = int(available_space_x / (2 * alien_width))
    return numbers_aliens_x - 2


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height)) - 1
    # print(number_rows)
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    import random
    res = random.choices([0,1])
    if res == [1]:
        aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 每个外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    # alien_width = alien.rect.width
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # numbers_aliens_x = int(available_space_x / (2 * alien_width))
    numbers_aliens_x = get_numbers_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建第一行外星人
    # for alien_number in range(numbers_aliens_x):
    #     # alien = Alien(ai_settings, screen)
    #     # alien.x = alien_width + 2 * alien_width * alien_number
    #     # alien.rect.x = alien.x
    #     # aliens.add(alien)
    #     create_aline(ai_settings, screen, aliens, alien_number)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(numbers_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达子弹限制， 就发射一颗子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:    # 检测 KEYDOWN 事件 即 键盘按下事件
            # if event.key == pygame.K_RIGHT:   # 检测按键是否是特定按键  此处是指 右箭头方形按键
            #     # 向右移动飞船，每次移动 1 个像素
            #     ship.rect.centerx += 1
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = True
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = True
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:        # 检测 KEYDOWN 事件 即 键盘松开事件
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = False
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击 Play 按钮时开始游戏"""
    # if play_button.rect.collidepoint(mouse_x, mouse_y):  # collidepoint 检测鼠标单击位置是否在 play 按钮的 rect 内
    button_checked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_checked and not stats.game_active:     # 仅当玩家单击按钮且游戏处于非活动状态时，才重新开始游戏
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, alien, bullets, play_button):
    """更新屏幕上的图像 ，并切换到新屏幕"""
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)  # 用背景色填充屏幕  screen.fill 只接受一个实参：一种颜色

    # 在飞船和外星人后面重绘子弹
    for bullet in bullets:
        bullet.draw_bullet()

    ship.blitme()

    # 绘制编组中的每个外星人
    alien.draw(screen)

    # 如果游戏处于非活动状态，就绘制 Play 的按钮
    if not stats.game_active:
        play_button.draw_buttton()

    # 显示得分
    sb.show_score()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中外星人
    # 如果是这样，就删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并提高游戏等级且新建一群外星人
        bullets.empty()         # empty 删除编组中剩下
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:

        # 将 Ship_left 减 1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕的底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查外星人是否到达了屏幕的底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # """更新外星人群中所有外星人的位置"""
    # aliens.update()
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 检查外星人是否到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
