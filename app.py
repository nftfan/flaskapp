from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual API key from PolygonScan
API_KEY = 'FZIZE7TZZ47WQMBK9YHRM31DWW6CZF8QU6'

@app.route('/get_subfan_score', methods=['GET'])
def get_subfan_score():
    wallet_address = request.args.get('wallet_address', '').strip()
    if not wallet_address:
        return jsonify({"error": "Please enter a valid wallet address."}), 400

    # PolygonScan API endpoint for token balance
    url = f'https://api.polygonscan.com/api'
    
    params = {
        'module': 'account',
        'action': 'tokenbalance',
        'contractaddress': '0x2017fcaea540d2925430586dc92818035bfc2f50',  # Token contract address
        'address': wallet_address,
        'tag': 'latest',
        'apikey': API_KEY
    }

    try:
        # Send GET request to PolygonScan API
        response = requests.get(url, params=params)
        data = response.json()

        # Check if response contains error
        if data['status'] == '0':
            return jsonify({"error": data['message']}), 400

        # Extract token balance (Subfan Score equivalent)
        subfan_score = int(data['result'])

        return jsonify({"wallet_address": wallet_address, "subfan_score": subfan_score})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
