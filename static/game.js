class TetrisGame {
    constructor() {
        this.gameBoard = document.getElementById('gameBoard');
        this.scoreDisplay = document.getElementById('score');
        this.levelDisplay = document.getElementById('level');
        this.linesDisplay = document.getElementById('lines');
        this.nextPieceDisplay = document.getElementById('nextPiece');
        this.startButton = document.getElementById('startButton');
        this.pauseButton = document.getElementById('pauseButton');
        this.gameOverModal = document.getElementById('gameOverModal');
        this.retryButton = document.getElementById('retryButton');
        
        this.isRunning = false;
        this.isPaused = false;
        this.gameState = null;
        this.gameSpeed = 500; // ms
        this.gameLoopInterval = null;
        
        this.setupEventListeners();
        this.initializeBoard();
    }
    
    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.startGame());
        this.pauseButton.addEventListener('click', () => this.togglePause());
        this.retryButton.addEventListener('click', () => this.startGame());
        
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }
    
    async initializeBoard() {
        // Get initial game state
        const response = await fetch('/api/game/new');
        this.gameState = await response.json();
        this.renderBoard();
        this.updateUI();
    }
    
    async startGame() {
        await this.initializeBoard();
        this.isRunning = true;
        this.isPaused = false;
        this.gameOverModal.style.display = 'none';
        
        this.startButton.disabled = true;
        this.pauseButton.disabled = false;
        
        this.gameLoopInterval = setInterval(() => this.gameLoop(), this.gameSpeed);
    }
    
    togglePause() {
        this.isPaused = !this.isPaused;
        this.pauseButton.textContent = this.isPaused ? '再開' : '一時停止';
        
        if (this.isPaused) {
            clearInterval(this.gameLoopInterval);
        } else {
            this.gameLoopInterval = setInterval(() => this.gameLoop(), this.gameSpeed);
        }
    }
    
    async gameLoop() {
        if (!this.isRunning || this.isPaused) return;
        
        try {
            const response = await fetch('/api/game/tick', { method: 'POST' });
            this.gameState = await response.json();
            
            this.renderBoard();
            this.updateUI();
            
            if (this.gameState.game_over) {
                this.endGame();
            }
        } catch (error) {
            console.error('ゲームループエラー:', error);
        }
    }
    
    async handleKeyPress(event) {
        if (!this.isRunning || this.isPaused) return;
        
        let direction = null;
        
        switch (event.key) {
            case 'ArrowLeft':
                direction = 'left';
                event.preventDefault();
                break;
            case 'ArrowRight':
                direction = 'right';
                event.preventDefault();
                break;
            case 'ArrowDown':
                direction = 'down';
                event.preventDefault();
                break;
            case 'ArrowUp':
                direction = 'rotate';
                event.preventDefault();
                break;
            case ' ':
                direction = 'drop';
                event.preventDefault();
                break;
        }
        
        if (direction) {
            try {
                const response = await fetch(`/api/game/move/${direction}`, { method: 'POST' });
                this.gameState = await response.json();
                this.renderBoard();
                this.updateUI();
            } catch (error) {
                console.error('移動エラー:', error);
            }
        }
    }
    
    renderBoard() {
        // Clear the board
        this.gameBoard.innerHTML = '';
        
        // Get piece coordinates
        const currentPieceCoords = new Set();
        if (this.gameState.piece && this.gameState.piece.length > 0) {
            this.gameState.piece.forEach(([x, y]) => {
                const boardX = this.gameState.piece_x + x;
                const boardY = this.gameState.piece_y + y;
                if (boardX >= 0 && boardX < 10 && boardY >= 0 && boardY < 20) {
                    currentPieceCoords.add(`${boardY},${boardX}`);
                }
            });
        }
        
        // Render board blocks
        for (let y = 0; y < 20; y++) {
            for (let x = 0; x < 10; x++) {
                const block = document.createElement('div');
                block.className = 'board-block';
                
                const key = `${y},${x}`;
                const isCurrentPiece = currentPieceCoords.has(key);
                const boardValue = this.gameState.board[y][x];
                
                if (isCurrentPiece) {
                    block.classList.add('filled', 'current');
                    block.classList.add(this.gameState.piece_type);
                } else if (boardValue !== 0) {
                    block.classList.add('filled');
                    // Determine piece type from board value
                    const colors = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
                    const pieceType = colors[Math.abs(boardValue) % colors.length];
                    block.classList.add(pieceType);
                }
                
                this.gameBoard.appendChild(block);
            }
        }
    }
    
    renderNextPiece() {
        this.nextPieceDisplay.innerHTML = '';
        
        if (!this.gameState.next_piece) return;
        
        // Create a 4x4 grid for the next piece
        for (let y = 0; y < 4; y++) {
            for (let x = 0; x < 4; x++) {
                const block = document.createElement('div');
                block.className = 'next-piece-block';
                
                // Check if any piece block occupies this position
                // This is simplified - you might need to implement proper piece data mapping
                
                this.nextPieceDisplay.appendChild(block);
            }
        }
        
        // テキストラベルの代わりに追加
        this.nextPieceDisplay.innerHTML = `<div style="grid-column: 1/-1; display: flex; align-items: center; justify-content: center; color: #667eea; font-weight: bold; font-size: 1.2em;">${this.gameState.next_piece}</div>`;
    }
    
    updateUI() {
        this.scoreDisplay.textContent = this.gameState.score;
        this.levelDisplay.textContent = this.gameState.level;
        this.linesDisplay.textContent = this.gameState.lines;
        this.renderNextPiece();
    }
    
    endGame() {
        this.isRunning = false;
        clearInterval(this.gameLoopInterval);
        
        this.startButton.disabled = false;
        this.pauseButton.disabled = true;
        
        document.getElementById('finalScore').textContent = this.gameState.score;
        this.gameOverModal.style.display = 'flex';
    }
}

// ページ読み込み時にゲームを初期化
document.addEventListener('DOMContentLoaded', () => {
    window.game = new TetrisGame();
});
