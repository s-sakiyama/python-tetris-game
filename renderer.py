"""
テトリスゲームレンダラー - ゲーム状態の描画
"""

import pygame
from typing import List, Tuple, Optional
from game_logic import PIECES

class GameRenderer:
    """テトリスゲームの描画を処理。"""
    
    def __init__(self, width: int, height: int, block_size: int = 30):
        """レンダラーを初期化。"""
        self.width = width
        self.height = height
        self.block_size = block_size
        
        # Colors
        self.COLOR_BG = (20, 20, 40)
        self.COLOR_GRID = (50, 50, 70)
        self.COLOR_PIECE = (200, 200, 200)
        self.COLOR_TEXT = (255, 255, 255)
        
        # Screen dimensions
        self.screen_width = width * block_size + 200
        self.screen_height = height * block_size + 40
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")
        
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
    
    def draw(self, game) -> None:
        """ゲーム状態を描画。"""
        self.screen.fill(self.COLOR_BG)
        
        # Draw game board
        self._draw_board(game)
        
        # Draw current piece
        self._draw_current_piece(game)
        
        # Draw UI
        self._draw_ui(game)
    
    def _draw_board(self, game) -> None:
        """ゲームボードを描画。"""
        board = game.get_board()
        
        # Draw grid and filled blocks
        for y in range(game.height):
            for x in range(game.width):
                rect = pygame.Rect(
                    x * self.block_size + 10,
                    y * self.block_size + 10,
                    self.block_size,
                    self.block_size
                )
                
                # Draw grid
                pygame.draw.rect(self.screen, self.COLOR_GRID, rect, 1)
                
                # Draw filled blocks
                if board[y][x] != 0:
                    color = self._get_color_from_id(board[y][x])
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, self.COLOR_GRID, rect, 1)
    
    def _draw_current_piece(self, game) -> None:
        """現在落下中のピースを描画。"""
        piece = game.get_current_piece()
        if piece is None:
            return
        
        piece_x, piece_y = game.get_piece_position()
        piece_type = game.current_piece_type
        color = PIECES[piece_type]['color']
        
        for block_x, block_y in piece:
            board_x = piece_x + block_x
            board_y = piece_y + block_y
            
            if 0 <= board_y < game.height:
                rect = pygame.Rect(
                    board_x * self.block_size + 10,
                    board_y * self.block_size + 10,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.COLOR_GRID, rect, 1)
    
    def _draw_ui(self, game) -> None:
        """ユーザーインターフェース要素(スコア、レベル、次ピース)を描画。"""
        ui_x = game.width * self.block_size + 30
        
        # Title
        title = self.title_font.render("TETRIS", True, self.COLOR_TEXT)
        self.screen.blit(title, (ui_x, 10))
        
        # Score
        score_text = self.font.render(f"Score: {game.score}", True, self.COLOR_TEXT)
        self.screen.blit(score_text, (ui_x, 50))
        
        # Level
        level_text = self.font.render(f"Level: {game.level}", True, self.COLOR_TEXT)
        self.screen.blit(level_text, (ui_x, 80))
        
        # Lines
        lines_text = self.font.render(f"Lines: {game.lines_cleared}", True, self.COLOR_TEXT)
        self.screen.blit(lines_text, (ui_x, 110))
        
        # Next piece
        next_label = self.font.render("Next:", True, self.COLOR_TEXT)
        self.screen.blit(next_label, (ui_x, 150))
        
        # Draw next piece preview
        next_piece_type = game.get_next_piece()
        if next_piece_type:
            next_piece = PIECES[next_piece_type]['shape']
            next_color = PIECES[next_piece_type]['color']
            
            for block_x, block_y in next_piece:
                rect = pygame.Rect(
                    ui_x + block_x * 20 + 10,
                    180 + block_y * 20,
                    20,
                    20
                )
                pygame.draw.rect(self.screen, next_color, rect)
                pygame.draw.rect(self.screen, self.COLOR_GRID, rect, 1)
    
    def _get_color_from_id(self, color_id: int) -> Tuple[int, int, int]:
        """色IDから色を取得。"""
        colors = [
            (0, 255, 255),      # I - Cyan
            (255, 255, 0),      # O - Yellow
            (128, 0, 128),      # T - Purple
            (0, 255, 0),        # S - Green
            (255, 0, 0),        # Z - Red
            (0, 0, 255),        # J - Blue
            (255, 165, 0),      # L - Orange
        ]
        return colors[color_id % len(colors)]
