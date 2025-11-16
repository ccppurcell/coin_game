import pygame

from coin_game.main import (
        Object, Robot, Monster, Coin, Door, border_w, border_h, height,
        width, field_w, field_h)

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

def test_coin_never_spawns_near_player():

    #init objects
    player = Robot()
    coin = Coin()

    for i in range(1,10):
        player.quadrant = i
        coin.loc(player.quadrant)
        assert coin.quadrant != player.quadrant

def test_door_never_spawns_near_player():

    #init objects
    player = Robot()
    door = Door()

    for i in range(1,10):
        player.quadrant = i
        door.loc(player.quadrant)
        assert door.quadrant != player.quadrant

def test_quadrant_bigger_than_player():

    #init objects
    player = Robot()

    assert field_w//3 > player.width
    assert field_h//3 > player.height
