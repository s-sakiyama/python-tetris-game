"""
テトリスゲームロジック - コアゲーム機構
"""

import random
from collections import deque
from typing import List, Tuple, Optional

# テトリスピース (Tetrominoes)
PIECES = {
    'I': {'shape': [(0, 0), (1, 0), (2, 0), (3, 0)], 'color': (0, 255, 255)},
    'O': {'shape': [(0, 0), (1, 0), (0, 1), (1, 1)], 'color': (255, 255, 0)},
    'T': {'shape': [(1, 0), (0, 1), (1, 1), (2, 1)], 'color': (128, 0, 128)},
    'S': {'shape': [(1, 0), (2, 0), (0, 1), (1, 1)], 'color': (0, 255, 0)},
    'Z': {'shape': [(0, 0), (1, 0), (1, 1), (2, 1)], 'color': (255, 0, 0)},
    'J': {'shape': [(0, 0), (0, 1), (1, 1), (2, 1)], 'color': (0, 0, 255)},
    'L': {'shape': [(2, 0), (0, 1), (1, 1), (2, 1)], 'color': (255, 165, 0)},
}

class TetrisGame:
    """メインのテトリスゲームクラス"""
    
    def __init__(self, width: int = 10, height: int = 20):
        """ゲームボードと状態を初期化"""
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = None
        self.current_piece_type = None
        self.current_piece_x = 0
        self.current_piece_y = 0
        self.next_piece_type = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.piece_colors = {}
        
        self.spawn_next_piece()
    
    def get_random_piece(self) -> str:
        """ランダムなピースタイプを取得"""
        return random.choice(list(PIECES.keys()))
    
    def spawn_next_piece(self) -> bool:
        """ボード上部に次のピースをスポーン"""
        if self.next_piece_type is None:
            self.next_piece_type = self.get_random_piece()
        
        self.current_piece_type = self.next_piece_type
        self.next_piece_type = self.get_random_piece()
        
        piece_data = PIECES[self.current_piece_type]
        self.current_piece = piece_data['shape'][:]
        self.current_piece_x = self.width // 2 - 2
        self.current_piece_y = 0
        self.piece_colors[id(self.current_piece)] = piece_data['color']
        
        # Check if spawn position is valid
        if not self._is_valid_position(self.current_piece, self.current_piece_x, self.current_piece_y):
            return False
        
        return True
    
    def _is_valid_position(self, piece: List[Tuple[int, int]], x: int, y: int) -> bool:
        """ピースの位置が有効かチェック"""
        for block_x, block_y in piece:
            new_x = x + block_x
            new_y = y + block_y
            
            if new_x < 0 or new_x >= self.width or new_y >= self.height:
                return False
            
            if new_y >= 0 and self.board[new_y][new_x] != 0:
                return False
        
        return True
    
    def _rotate_piece(self, piece: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """ピースを90度時計回りに回転"""
        # For O piece (square), rotation does nothing
        if len(piece) == 4:
            coords = set(piece)
            if coords == {(0, 0), (1, 0), (0, 1), (1, 1)}:
                return piece  # O piece doesn't rotate
        
        rotated = [(-y, x) for x, y in piece]
        # Normalize to positive coordinates
        min_x = min(x for x, y in rotated)
        min_y = min(y for x, y in rotated)
        # Sort to maintain consistent ordering
        normalized = sorted([(x - min_x, y - min_y) for x, y in rotated])
        return normalized
    
    def rotate_piece(self) -> bool:
        """Rotate the current piece."""
        rotated = self._rotate_piece(self.current_piece)
        
        if self._is_valid_position(rotated, self.current_piece_x, self.current_piece_y):
            self.current_piece = rotated
            return True
        
        return False
    
    def move_piece_left(self) -> bool:
        """Move the current piece left."""
        if self._is_valid_position(self.current_piece, self.current_piece_x - 1, self.current_piece_y):
            self.current_piece_x -= 1
            return True
        return False
    
    def move_piece_right(self) -> bool:
        """Move the current piece right."""
        if self._is_valid_position(self.current_piece, self.current_piece_x + 1, self.current_piece_y):
            self.current_piece_x += 1
            return True
        return False
    
    def move_piece_down(self) -> bool:
        """Move the current piece down."""
        if self._is_valid_position(self.current_piece, self.current_piece_x, self.current_piece_y + 1):
            self.current_piece_y += 1
            return True
        else:
            # Piece can't move down, lock it in place
            self._lock_piece()
            return False
    
    def hard_drop(self) -> bool:
        """Drop the piece all the way down."""
        while self.move_piece_down():
            self.score += 1
        return True
    
    def _lock_piece(self) -> None:
        """Lock the current piece in place on the board."""
        piece_color = self.piece_colors.get(id(self.current_piece), (255, 255, 255))
        color_id = self._get_color_id(piece_color)
        
        for block_x, block_y in self.current_piece:
            board_x = self.current_piece_x + block_x
            board_y = self.current_piece_y + block_y
            
            if 0 <= board_y < self.height and 0 <= board_x < self.width:
                self.board[board_y][board_x] = color_id
        
        self._clear_lines()
    
    def _get_color_id(self, color: Tuple[int, int, int]) -> int:
        """Get a unique ID for a color."""
        return hash(color) % 1000 + 1
    
    def _clear_lines(self) -> None:
        """完了したラインをチェックしてクリア"""
        lines_to_clear = []
        
        for y in range(self.height):
            if all(self.board[y][x] != 0 for x in range(self.width)):
                lines_to_clear.append(y)
        
        for y in sorted(lines_to_clear, reverse=True):
            del self.board[y]
            self.board.insert(0, [0 for _ in range(self.width)])
        
        if lines_to_clear:
            num_lines = len(lines_to_clear)
            self.lines_cleared += num_lines
            # Score calculation
            score_table = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += score_table.get(num_lines, 0) * self.level
            self.level = 1 + self.lines_cleared // 10
    
    def get_board(self) -> List[List[int]]:
        """現在のボード状態を取得"""
        return [row[:] for row in self.board]
    
    def get_current_piece(self) -> Optional[List[Tuple[int, int]]]:
        """現在の落下中のピースを取得"""
        return self.current_piece
    
    def get_piece_position(self) -> Tuple[int, int]:
        """現在のピース位置を取得"""
        return (self.current_piece_x, self.current_piece_y)
    
    def get_next_piece(self) -> str:
        """次のピースタイプを取得"""
        return self.next_piece_type
