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
        
        // モバイルコントロール要素
        this.leftBtn = document.getElementById('leftBtn');
        this.rightBtn = document.getElementById('rightBtn');
        this.downBtn = document.getElementById('downBtn');
        this.upBtn = document.getElementById('upBtn');
        this.rotateBtn = document.getElementById('rotateBtn');
        this.dropBtn = document.getElementById('dropBtn');
        
        this.isRunning = false;
        this.isPaused = false;
        this.gameState = null;
        this.gameSpeed = 500; // ms
        this.gameLoopInterval = null;
        
        this.setupEventListeners();
        this.setupMobileControls();
        this.initializeBoard();
    }
    
    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.startGame());
        this.pauseButton.addEventListener('click', () => this.togglePause());
        this.retryButton.addEventListener('click', () => this.startGame());
        
        // キーボード入力
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // P キーで一時停止
        document.addEventListener('keydown', (e) => {
            if (e.key === 'p' || e.key === 'P') {
                if (this.isRunning) {
                    this.togglePause();
                }
            }
        });
    }
    
    setupMobileControls() {
        if (!this.leftBtn) return; // モバイルボタンが存在しない場合はスキップ
        
        // タッチイベント対応
        this.setupMobileButton(this.leftBtn, () => this.moveLeft());
        this.setupMobileButton(this.rightBtn, () => this.moveRight());
        this.setupMobileButton(this.downBtn, () => this.moveDown());
        this.setupMobileButton(this.upBtn, () => this.moveUp());
        this.setupMobileButton(this.rotateBtn, () => this.rotate());
        this.setupMobileButton(this.dropBtn, () => this.drop());
    }
    
    setupMobileButton(button, callback) {
        if (!button) return;
        
        let isPressed = false;
        let pressTimer = null;
        
        const handleStart = (e) => {
            e.preventDefault();
            isPressed = true;
            callback();
            
            // 連続入力対応：長押しで繰り返す
            pressTimer = setInterval(callback, 100);
        };
        
        const handleEnd = (e) => {
            e.preventDefault();
            isPressed = false;
            if (pressTimer) clearInterval(pressTimer);
        };
        
        // マウス & タッチイベント
        button.addEventListener('mousedown', handleStart);
        button.addEventListener('mouseup', handleEnd);
        button.addEventListener('mouseleave', handleEnd);
        button.addEventListener('touchstart', handleStart);
        button.addEventListener('touchend', handleEnd);
    }
    
    async moveLeft() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('left');
    }
    
    async moveRight() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('right');
    }
    
    async moveDown() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('down');
    }
    
    async moveUp() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('rotate');
    }
    
    async rotate() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('rotate');
    }
    
    async drop() {
        if (!this.isRunning || this.isPaused) return;
        await this.makeMove('drop');
    }
    
    async makeMove(direction) {
        try {
            const response = await fetch(`/api/game/move/${direction}`, { method: 'POST' });
            this.gameState = await response.json();
            this.renderBoard();
            this.updateUI();
        } catch (error) {
            console.error('移動エラー:', error);
        }
    }
    
    async initializeBoard() {
        try {
            const response = await fetch('/api/game/new');
            this.gameState = await response.json();
            this.renderBoard();
            this.updateUI();
        } catch (error) {
            console.error('ボード初期化エラー:', error);
        }
    }
    
    async startGame() {
        await this.initializeBoard();
        this.isRunning = true;
        this.isPaused = false;
        this.gameOverModal.style.display = 'none';
        
        this.startButton.disabled = true;
        this.pauseButton.disabled = false;
        this.pauseButton.textContent = '⏸ 一時停止';
        
        this.gameLoopInterval = setInterval(() => this.gameLoop(), this.gameSpeed);
    }
    
    togglePause() {
        this.isPaused = !this.isPaused;
        this.pauseButton.textContent = this.isPaused ? '▶ 再開' : '⏸ 一時停止';
        
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
            await this.makeMove(direction);
        }
    }
    
    renderBoard() {
        // ボードをクリア
        this.gameBoard.innerHTML = '';
        
        // ピースの座標を取得
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
        
        // ボードブロックをレンダリング
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
                    // ボード値からピースタイプを判定
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
        
        // 次のピースを4x4グリッドで表示
        for (let y = 0; y < 4; y++) {
            for (let x = 0; x < 4; x++) {
                const block = document.createElement('div');
                block.className = 'next-piece-block';
                
                this.nextPieceDisplay.appendChild(block);
            }
        }
        
        // 日本語でピースのラベルを表示
        this.nextPieceDisplay.innerHTML = `<div style="grid-column: 1/-1; display: flex; align-items: center; justify-content: center; color: #667eea; font-weight: bold; font-size: 1.2em;">${this.gameState.next_piece}</div>`;
    }
    
    updateUI() {
        this.scoreDisplay.textContent = this.gameState.score.toLocaleString();
        this.levelDisplay.textContent = this.gameState.level;
        this.linesDisplay.textContent = this.gameState.lines;
        this.renderNextPiece();
    }
    
    endGame() {
        this.isRunning = false;
        clearInterval(this.gameLoopInterval);
        
        this.startButton.disabled = false;
        this.pauseButton.disabled = true;
        this.startButton.textContent = '▶ 開始';
        
        document.getElementById('finalScore').textContent = this.gameState.score.toLocaleString();
        document.getElementById('finalLevel').textContent = this.gameState.level;
        document.getElementById('finalLines').textContent = this.gameState.lines;
        
        this.gameOverModal.style.display = 'flex';
    }
}

// ページ読み込み時にゲームを初期化
document.addEventListener('DOMContentLoaded', () => {
    window.game = new TetrisGame();
});
