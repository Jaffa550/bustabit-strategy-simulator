from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    bankroll = data['bankroll']
    number_of_plays = data['number_of_plays']
    bet = data['bet']
    cash_out_target = data['cash_out_target']
    strategy = data['strategy']
    
    results = []
    initial_bet = bet

    for _ in range(number_of_plays):
        crash_point = random.uniform(1, 100)  # Simulated crash multiplier
        if crash_point >= cash_out_target:
            profit = bet * (cash_out_target - 1)
            bankroll += profit
            results.append({'game': len(results) + 1, 'outcome': 'Win', 'change': profit, 'bankroll': bankroll})
        else:
            bankroll -= bet
            results.append({'game': len(results) + 1, 'outcome': 'Loss', 'change': -bet, 'bankroll': bankroll})
        
        # Strategy adjustment
        if strategy == "martingale" and results[-1]['outcome'] == 'Loss':
            bet *= 2
        else:
            bet = initial_bet

        if bankroll <= 0:
            break  # Stop if bankrupt

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
