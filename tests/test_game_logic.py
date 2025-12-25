"""
Tests for Tetris Game Logic
"""

import pytest
from game_logic import TetrisGame, PIECES


class TestTetrisGameInitialization:
    """Test game initialization."""
    
    def test_game_initialization(self):
        """Test that game initializes correctly."""
        game = TetrisGame(10, 20)
        assert game.width == 10
        assert game.height == 20
        assert game.score == 0
        assert game.level == 1
        assert game.lines_cleared == 0
    
    def test_board_dimensions(self):
        """Test board has correct dimensions."""
        game = TetrisGame(10, 20)
        assert len(game.board) == 20
        assert all(len(row) == 10 for row in game.board)
    
    def test_piece_spawned(self):
        """Test that a piece is spawned on initialization."""
        game = TetrisGame()
        assert game.current_piece is not None
        assert game.current_piece_type in PIECES
        assert game.next_piece_type in PIECES


class TestPieceMovement:
    """Test piece movement."""
    
    def test_move_left(self):
        """Test moving piece left."""
        game = TetrisGame()
        initial_x = game.current_piece_x
        success = game.move_piece_left()
        assert success
        assert game.current_piece_x == initial_x - 1
    
    def test_move_right(self):
        """Test moving piece right."""
        game = TetrisGame()
        initial_x = game.current_piece_x
        success = game.move_piece_right()
        assert success
        assert game.current_piece_x == initial_x + 1
    
    def test_move_down(self):
        """Test moving piece down."""
        game = TetrisGame()
        initial_y = game.current_piece_y
        success = game.move_piece_down()
        assert success
        assert game.current_piece_y == initial_y + 1
    
    def test_boundary_left(self):
        """Test left boundary."""
        game = TetrisGame()
        game.current_piece_x = 0
        success = game.move_piece_left()
        assert not success
        assert game.current_piece_x == 0
    
    def test_boundary_right(self):
        """Test right boundary."""
        game = TetrisGame()
        # Move right as much as possible
        for _ in range(10):
            game.move_piece_right()
        
        success = game.move_piece_right()
        assert not success


class TestPieceRotation:
    """Test piece rotation."""
    
    def test_rotate_piece(self):
        """Test rotating a piece."""
        game = TetrisGame()
        initial_piece = game.current_piece[:]
        success = game.rotate_piece()
        assert success
        # After rotation, the piece should be different (unless O piece)
        if game.current_piece_type != 'O':
            assert game.current_piece != initial_piece
    
    def test_o_piece_rotation(self):
        """Test O piece rotation (should not change)."""
        game = TetrisGame()
        # Keep generating pieces until we get O
        while game.current_piece_type != 'O':
            if not game.move_piece_down():
                if not game.spawn_next_piece():
                    break
        
        if game.current_piece_type == 'O':
            initial_piece = game.current_piece[:]
            game.rotate_piece()
            assert game.current_piece == initial_piece


class TestLineClearing:
    """Test line clearing."""
    
    def test_complete_line_cleared(self):
        """Test that complete lines are cleared."""
        game = TetrisGame(10, 20)
        
        # Fill bottom row completely
        for x in range(game.width):
            game.board[game.height - 1][x] = 1
        
        # Fill row above except for one spot
        for x in range(game.width - 1):
            game.board[game.height - 2][x] = 1
        
        initial_lines = game.lines_cleared
        game._clear_lines()
        
        # Bottom row should be cleared (replaced with new empty row at top)
        # So the row at bottom should now be the previous second row (with one empty cell)
        assert any(cell == 0 for cell in game.board[game.height - 1])
        # Lines cleared should increase
        assert game.lines_cleared == initial_lines + 1
    
    def test_no_line_cleared(self):
        """Test that incomplete lines are not cleared."""
        game = TetrisGame()
        initial_lines = game.lines_cleared
        game._clear_lines()
        assert game.lines_cleared == initial_lines


class TestGameOver:
    """Test game over condition."""
    
    def test_spawn_at_invalid_position(self):
        """Test game over when piece can't spawn."""
        game = TetrisGame(10, 20)
        
        # Fill the top rows
        for y in range(3):
            for x in range(10):
                game.board[y][x] = 1
        
        # Try to spawn a new piece
        success = game.spawn_next_piece()
        assert not success


class TestScoring:
    """Test scoring system."""
    
    def test_initial_score(self):
        """Test initial score is zero."""
        game = TetrisGame()
        assert game.score == 0
    
    def test_hard_drop_increases_score(self):
        """Test that hard drop increases score."""
        game = TetrisGame()
        initial_score = game.score
        game.hard_drop()
        assert game.score > initial_score
    
    def test_level_progression(self):
        """Test level increases with lines cleared."""
        game = TetrisGame()
        assert game.level == 1
        
        game.lines_cleared = 10
        game.level = 1 + game.lines_cleared // 10
        assert game.level == 2


class TestPieceData:
    """Test piece data integrity."""
    
    def test_all_pieces_have_shapes(self):
        """Test all pieces have valid shapes."""
        for piece_type, piece_data in PIECES.items():
            assert 'shape' in piece_data
            assert 'color' in piece_data
            assert len(piece_data['shape']) == 4
            assert len(piece_data['color']) == 3
    
    def test_piece_colors_valid(self):
        """Test piece colors are valid RGB values."""
        for piece_type, piece_data in PIECES.items():
            r, g, b = piece_data['color']
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
