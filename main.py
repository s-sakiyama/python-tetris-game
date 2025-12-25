#!/usr/bin/env python3
"""
Tetris Game - Main Entry Point
"""

import pygame
from game_logic import TetrisGame
from renderer import GameRenderer
import sys

def main():
    """Initialize and run the Tetris game."""
    pygame.init()
    
    # Game configuration
    game_width = 10
    game_height = 20
    block_size = 30
    
    # Create game and renderer
    game = TetrisGame(game_width, game_height)
    renderer = GameRenderer(game_width, game_height, block_size)
    
    clock = pygame.time.Clock()
    running = True
    drop_time = 0
    drop_interval = 30  # frames
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_piece_right()
                elif event.key == pygame.K_DOWN:
                    game.move_piece_down()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_q:
                    running = False
        
        # Auto drop piece
        drop_time += 1
        if drop_time >= drop_interval:
            if not game.move_piece_down():
                if not game.spawn_next_piece():
                    print(f"Game Over! Score: {game.score}")
                    running = False
            drop_time = 0
        
        # Render game
        renderer.draw(game)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
