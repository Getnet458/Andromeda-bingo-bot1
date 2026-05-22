# webapp_server.py - Fixed: Players and Derash start at 0

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import time
import threading
from datetime import datetime
from collections import defaultdict

app = Flask(__name__, static_folder='webapp')
CORS(app)

# ========== DATA STORAGE ==========
users = defaultdict(lambda: {
    'balance': 385.0,
    'total_wagered': 0,
    'total_won': 0,
    'games_played': 0,
    'games_won': 0
})

owner_data = {
    'balance': 0.0,
    'total_commission_earned': 0.0,
    'total_games_hosted': 0,
    'total_prize_pool': 0.0
}

COMMISSION_RATE = 0.20

# Game rooms - START WITH 0 PLAYERS AND 0 PRIZE POOL!
game_rooms = {
    'g10': {'stake': 10, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0},
    'g20': {'stake': 20, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0},
    'g50': {'stake': 50, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0}
}

# Active game states
active_calls = defaultdict(lambda: {'numbers': [], 'current': None, 'active': False})

# Track active players in each game
active_players = defaultdict(list)

# ========== HELPER FUNCTIONS ==========

def generate_cartela(cartela_id):
    """Generate deterministic Bingo card based on cartela number"""
    random.seed(cartela_id * 0x9e3779b9 + 0x6b43a9c5)
    
    ranges = [[1,15], [16,30], [31,45], [46,60], [61,75]]
    cols = []
    for lo, hi in ranges:
        nums = list(range(lo, hi + 1))
        random.shuffle(nums)
        cols.append(nums[:5])
    
    grid = []
    for r in range(5):
        row = [cols[c][r] for c in range(5)]
        grid.append(row)
    grid[2][2] = 'FREE'
    
    return grid

def start_game_auto_call(game_id):
    """Start automatic number calling for a game"""
    def auto_call():
        call_state = active_calls.get(game_id, {'numbers': [], 'current': None, 'active': True})
        if not call_state.get('active', True):
            return
        
        # Wait 5 seconds between calls
        time.sleep(5)
        
        # Generate random number 1-75 not yet called
        available = [n for n in range(1, 76) if n not in call_state['numbers']]
        if available:
            new_number = random.choice(available)
            call_state['numbers'].append(new_number)
            call_state['current'] = new_number
            active_calls[game_id] = call_state
        
        # Continue calling if game is active and has players
        if game_id in game_rooms and game_rooms[game_id]['state'] == 'active' and len(active_players[game_id]) > 0:
            threading.Thread(target=auto_call, daemon=True).start()
    
    threading.Thread(target=auto_call, daemon=True).start()

# ========== API ENDPOINTS ==========

@app.route('/')
def index():
    return send_from_directory('webapp', 'index.html')

@app.route('/api/rooms', methods=['GET', 'POST'])
def get_rooms():
    """Return current game rooms status"""
    rooms = []
    for room_id, room in game_rooms.items():
        rooms.append({
            'id': room_id,
            'stake': room['stake'],
            'players': room['players'],
            'state': room['state'],
            'cd': room['cd'],
            'prize_pool': room['prize_pool']
        })
    
    # Get balance for current user
    balance = 385.0
    return jsonify({
        'rooms': rooms,
        'balance': balance
    })

@app.route('/api/join', methods=['POST'])
def join_game():
    """Join a game room"""
    data = request.json
    room_id = data.get('game_id')
    user_id = data.get('user_id', 'current')
    cartela_ids = data.get('cartela_ids', [])
    
    if room_id not in game_rooms:
        return jsonify({'error': 'Game not found'}), 404
    
    room = game_rooms[room_id]
    
    # Check if game is still joinable
    if room['state'] != 'lobby' and room['state'] != 'waiting':
        return jsonify({'error': 'Game already started'}), 400
    
    # Create user if not exists
    if user_id not in users:
        users[user_id] = {'balance': 385.0, 'total_wagered': 0, 'total_won': 0, 'games_played': 0, 'games_won': 0}
    
    # Check balance
    total_cost = room['stake'] * len(cartela_ids)
    if users[user_id]['balance'] < total_cost:
        return jsonify({'error': f'Insufficient balance! Need {total_cost} ETB'}), 400
    
    # Deduct balance
    users[user_id]['balance'] -= total_cost
    users[user_id]['total_wagered'] += total_cost
    users[user_id]['games_played'] += 1
    
    # Generate cartelas
    cartelas = []
    for cartela_id in cartela_ids:
        cartelas.append({
            'id': cartela_id,
            'grid': generate_cartela(cartela_id)
        })
    
    # Update room players and prize pool
    room['players'] += 1
    room['prize_pool'] = room['players'] * room['stake']
    
    # Track active player
    if user_id not in active_players[room_id]:
        active_players[room_id].append(user_id)
    
    # Start game if this is the first player
    if room['players'] == 1:
        room['state'] = 'active'
        # Start countdown
        def start_game():
            time.sleep(3)
            room['cd'] = 30
            if room_id not in active_calls:
                active_calls[room_id] = {'numbers': [], 'current': None, 'active': True}
            start_game_auto_call(room_id)
        threading.Thread(target=start_game, daemon=True).start()
    
    return jsonify({
        'success': True,
        'game_id': room_id,
        'stake': room['stake'],
        'prize_pool': room['prize_pool'],
        'players': room['players'],
        'cartelas': cartelas,
        'balance': users[user_id]['balance']
    })

@app.route('/api/game/next_number', methods=['POST'])
def next_number():
    """Get the next number for auto-calling"""
    data = request.json
    game_id = data.get('game_id')
    
    if game_id not in active_calls:
        return jsonify({'number': None, 'called_numbers': [], 'game_over': False})
    
    call_state = active_calls[game_id]
    current_number = call_state.get('current')
    
    return jsonify({
        'number': current_number,
        'called_numbers': call_state.get('numbers', []),
        'game_over': not call_state.get('active', True)
    })

@app.route('/api/game/bingo', methods=['POST'])
def claim_bingo():
    """Claim BINGO win"""
    data = request.json
    game_id = data.get('game_id')
    user_id = data.get('user_id', 'current')
    cartela_id = data.get('cartela_id')
    
    if game_id not in game_rooms:
        return jsonify({'error': 'Game not found'}), 404
    
    room = game_rooms[game_id]
    
    # Calculate winnings (80% to player, 20% owner)
    prize_pool = room['prize_pool']
    winnings = prize_pool * 0.80
    commission = prize_pool * 0.20
    
    # Update owner commission
    owner_data['balance'] += commission
    owner_data['total_commission_earned'] += commission
    owner_data['total_prize_pool'] += prize_pool
    owner_data['total_games_hosted'] += 1
    
    # Update user balance
    if user_id in users:
        users[user_id]['balance'] += winnings
        users[user_id]['total_won'] += winnings
        users[user_id]['games_won'] += 1
    
    # Mark game as finished
    room['state'] = 'finished'
    room['cd'] = 30
    
    # Clear active calls
    if game_id in active_calls:
        active_calls[game_id]['active'] = False
    
    # Schedule game restart after 30 seconds
    def restart_game():
        time.sleep(30)
        room['state'] = 'lobby'
        room['cd'] = 20
        room['players'] = 0
        room['prize_pool'] = 0
        active_players[game_id] = []
        if game_id in active_calls:
            active_calls[game_id] = {'numbers': [], 'current': None, 'active': False}
    
    threading.Thread(target=restart_game, daemon=True).start()
    
    return jsonify({
        'success': True,
        'win_amount': winnings,
        'new_balance': users.get(user_id, {}).get('balance', 0)
    })

@app.route('/api/balance', methods=['POST'])
def get_balance():
    data = request.json
    user_id = data.get('user_id', 'current')
    
    if user_id not in users:
        users[user_id] = {'balance': 385.0, 'total_wagered': 0, 'total_won': 0, 'games_played': 0, 'games_won': 0}
    
    return jsonify(users[user_id])

@app.route('/api/owner_balance', methods=['GET'])
def get_owner_balance():
    return jsonify({
        'owner_balance': owner_data['balance'],
        'total_commission_earned': owner_data['total_commission_earned'],
        'total_games_hosted': owner_data['total_games_hosted'],
        'total_prize_pool': owner_data['total_prize_pool'],
        'commission_rate': COMMISSION_RATE * 100
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_rooms():
    """Refresh game rooms status"""
    # Just return current status without artificially inflating numbers
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("🎮 ANDROMEDA BINGO SERVER")
    print("=" * 50)
    print("📍 http://localhost:5000")
    print("📊 Players and Derash start at 0 until someone joins!")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)