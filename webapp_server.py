# webapp_server.py - 20% Owner Commission, Auto-Deduct 24/7

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import time
import threading
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__, static_folder='webapp')
CORS(app)

# ========== DATA STORAGE ==========
users = defaultdict(lambda: {
    'balance': 100.0,  # Start with 100 ETB
    'total_wagered': 0,
    'total_won': 0,
    'games_played': 0,
    'games_won': 0
})

# Owner commission storage - PERSISTENT (saves to file)
OWNER_COMMISSION_RATE = 0.20  # 20% to owner, 80% to winner
owner_data = {
    'balance': 0.0,
    'total_commission_earned': 0.0,
    'total_games_hosted': 0,
    'total_prize_pool': 0.0
}

# Game rooms - start with 0 players
game_rooms = {
    'g10': {'stake': 10, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0},
    'g20': {'stake': 20, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0},
    'g50': {'stake': 50, 'players': 0, 'state': 'lobby', 'cd': 20, 'prize_pool': 0}
}

# Active game states
active_calls = defaultdict(lambda: {'numbers': [], 'current': None, 'active': False})
active_players = defaultdict(list)

# ========== PERSISTENT OWNER DATA (SAVES TO FILE) ==========

def save_owner_data():
    """Save owner commission data to file - survives server restart!"""
    try:
        with open('owner_data.json', 'w') as f:
            json.dump(owner_data, f)
        print(f"💰 Owner data saved: Balance = {owner_data['balance']:.2f} ETB")
    except Exception as e:
        print(f"Error saving owner data: {e}")

def load_owner_data():
    """Load owner commission data from file"""
    global owner_data
    try:
        if os.path.exists('owner_data.json'):
            with open('owner_data.json', 'r') as f:
                saved = json.load(f)
                owner_data.update(saved)
                print(f"✅ Loaded owner balance: {owner_data['balance']:.2f} ETB")
                print(f"✅ Total games hosted: {owner_data['total_games_hosted']}")
                print(f"✅ Total prize pool: {owner_data['total_prize_pool']:.2f} ETB")
        else:
            print("📁 No saved owner data found, starting fresh")
    except Exception as e:
        print(f"Error loading owner data: {e}")

# Load saved data on startup
load_owner_data()

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

def add_owner_commission(amount, game_stake, num_players):
    """Add commission to owner's balance and save immediately"""
    global owner_data
    owner_data['balance'] += amount
    owner_data['total_commission_earned'] += amount
    
    print(f"\n{'='*50}")
    print(f"💰 OWNER COMMISSION: +{amount:.2f} ETB")
    print(f"👑 Owner Balance: {owner_data['balance']:.2f} ETB")
    print(f"📊 Total Commission: {owner_data['total_commission_earned']:.2f} ETB")
    print(f"{'='*50}\n")
    
    # Save to file immediately (persistence!)
    save_owner_data()

def start_game_auto_call(game_id):
    """Start automatic number calling for a game"""
    def auto_call():
        call_state = active_calls.get(game_id, {'numbers': [], 'current': None, 'active': True})
        if not call_state.get('active', True):
            return
        
        time.sleep(5)
        
        available = [n for n in range(1, 76) if n not in call_state['numbers']]
        if available:
            new_number = random.choice(available)
            call_state['numbers'].append(new_number)
            call_state['current'] = new_number
            active_calls[game_id] = call_state
        
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
    
    return jsonify({
        'rooms': rooms,
        'balance': users.get('current', {}).get('balance', 100)
    })

@app.route('/api/join', methods=['POST'])
def join_game():
    """Join a game room - AUTO DEDUCTS STAKE FROM PLAYER"""
    data = request.json
    room_id = data.get('game_id')
    user_id = data.get('user_id', 'current')
    cartela_ids = data.get('cartela_ids', [])
    
    if room_id not in game_rooms:
        return jsonify({'error': 'Game not found'}), 404
    
    room = game_rooms[room_id]
    
    if room['state'] != 'lobby' and room['state'] != 'waiting':
        return jsonify({'error': 'Game already started'}), 400
    
    if user_id not in users:
        users[user_id] = {'balance': 100.0, 'total_wagered': 0, 'total_won': 0, 'games_played': 0, 'games_won': 0}
    
    # Calculate total cost
    total_cost = room['stake'] * len(cartela_ids)
    
    # CHECK BALANCE BEFORE DEDUCTING
    if users[user_id]['balance'] < total_cost:
        return jsonify({'error': f'Insufficient balance! Need {total_cost} ETB'}), 400
    
    # === AUTO DEDUCT STAKE FROM PLAYER ===
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
    
    if user_id not in active_players[room_id]:
        active_players[room_id].append(user_id)
    
    # Start game if first player
    if room['players'] == 1:
        room['state'] = 'active'
        def start_game():
            time.sleep(3)
            room['cd'] = 30
            if room_id not in active_calls:
                active_calls[room_id] = {'numbers': [], 'current': None, 'active': True}
            start_game_auto_call(room_id)
        threading.Thread(target=start_game, daemon=True).start()
    
    print(f"\n✅ Player joined {room['stake']} ETB game")
    print(f"💰 Stake deducted: {total_cost} ETB")
    print(f"💎 Player new balance: {users[user_id]['balance']:.2f} ETB")
    print(f"👥 Total players: {room['players']}")
    print(f"🏆 Prize pool: {room['prize_pool']:.2f} ETB\n")
    
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
    """Claim BINGO win - AUTO AWARDS 80% TO PLAYER, 20% TO OWNER"""
    data = request.json
    game_id = data.get('game_id')
    user_id = data.get('user_id', 'current')
    cartela_id = data.get('cartela_id')
    
    if game_id not in game_rooms:
        return jsonify({'error': 'Game not found'}), 404
    
    room = game_rooms[game_id]
    
    # Calculate distribution
    total_prize_pool = room['prize_pool']
    player_winnings = total_prize_pool * 0.80  # 80% to winner
    owner_commission = total_prize_pool * 0.20  # 20% to owner
    
    # === ADD COMMISSION TO OWNER ===
    add_owner_commission(owner_commission, room['stake'], room['players'])
    owner_data['total_games_hosted'] += 1
    owner_data['total_prize_pool'] += total_prize_pool
    save_owner_data()
    
    # === ADD WINNINGS TO PLAYER ===
    if user_id in users:
        users[user_id]['balance'] += player_winnings
        users[user_id]['total_won'] += player_winnings
        users[user_id]['games_won'] += 1
        new_balance = users[user_id]['balance']
    
    # Mark game as finished
    room['state'] = 'finished'
    room['cd'] = 30
    
    if game_id in active_calls:
        active_calls[game_id]['active'] = False
    
    print(f"\n{'='*50}")
    print(f"🎉 BINGO WINNER! 🎉")
    print(f"💰 Total Prize Pool: {total_prize_pool:.2f} ETB")
    print(f"🏆 Winner Gets: {player_winnings:.2f} ETB (80%)")
    print(f"👑 Owner Gets: {owner_commission:.2f} ETB (20%)")
    print(f"💎 Winner New Balance: {new_balance:.2f} ETB")
    print(f"👑 Owner Total Balance: {owner_data['balance']:.2f} ETB")
    print(f"{'='*50}\n")
    
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
        print(f"🔄 Game {room['stake']} ETB restarted for new players!")
    
    threading.Thread(target=restart_game, daemon=True).start()
    
    return jsonify({
        'success': True,
        'win_amount': player_winnings,
        'commission_amount': owner_commission,
        'new_balance': new_balance
    })

@app.route('/api/balance', methods=['POST'])
def get_balance():
    """Get user's current balance"""
    data = request.json
    user_id = data.get('user_id', 'current')
    
    if user_id not in users:
        users[user_id] = {'balance': 100.0, 'total_wagered': 0, 'total_won': 0, 'games_played': 0, 'games_won': 0}
    
    return jsonify(users[user_id])

@app.route('/api/owner_balance', methods=['GET'])
def get_owner_balance():
    """Get owner's commission balance (for /owner command in Telegram)"""
    return jsonify({
        'owner_balance': owner_data['balance'],
        'total_commission_earned': owner_data['total_commission_earned'],
        'total_games_hosted': owner_data['total_games_hosted'],
        'total_prize_pool': owner_data['total_prize_pool'],
        'commission_rate': OWNER_COMMISSION_RATE * 100
    })

@app.route('/api/owner/withdraw', methods=['POST'])
def owner_withdraw():
    """Withdraw owner commission (admin only)"""
    data = request.json
    amount = data.get('amount')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    if amount > owner_data['balance']:
        return jsonify({'error': 'Insufficient balance'}), 400
    
    owner_data['balance'] -= amount
    save_owner_data()
    
    print(f"💸 OWNER WITHDRAWAL: {amount:.2f} ETB")
    print(f"💰 Remaining: {owner_data['balance']:.2f} ETB")
    
    return jsonify({
        'success': True,
        'withdrawn': amount,
        'remaining': owner_data['balance']
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_rooms():
    """Refresh game rooms status"""
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 ANDROMEDA BINGO - 20% COMMERCIAL EDITION 🎮")
    print("=" * 60)
    print(f"💰 Commission Rate: {OWNER_COMMISSION_RATE * 100}% to Owner")
    print(f"📊 Winner Gets: {(1 - OWNER_COMMISSION_RATE) * 100}%")
    print(f"👑 Owner Balance: {owner_data['balance']:.2f} ETB")
    print(f"📍 Server: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)