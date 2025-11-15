import pygame

from coin_game.main import (
        Object, Robot, Monster, Coin, border_w, border_h, height, width)

def test_player_cannot_move_out_of_bounds():

    #init the player
    player = Robot()

    #first target is top right corner
    target1_x, target1_y = border_w, border_h

    #move player to target
    player.x, player.y = target1_x, target1_y

    #attempt to move player outside the border
    player.move_left()
    player.move_up()

    #player shouldn't move
    assert player.x == target1_x
    assert player.y == target1_y

    #second target is bottom left corner
    target2_x = width - border_w - player.width
    target2_y = height - border_h - player.height

    #move player to target
    player.x, player.y = target2_x, target2_y

    #attempt to move player outside the border
    player.move_right()
    player.move_down()
    
    #player shouldn't move
    assert player.x == target2_x
    assert player.y == target2_y

