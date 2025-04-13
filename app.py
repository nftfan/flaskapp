from flask import Flask, request, jsonify
import requests
import re
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_subfan_score', methods=['GET'])
def get_subfan_score():
    wallet_address = request.args.get('wallet_address', '').strip()  # Ensure we handle None properly
    if not wallet_address:
        return jsonify({"error": "Please enter a valid wallet address."}), 400

    url = f"https://polygonscan.com/token/token-analytics?m=dark&contractAddress=0x2017fcaea540d2925430586dc92818035bfc2f50&a={wallet_address}&lg=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        html = response.text

        # Extract the var plotData2ab = eval(...) part using regex
        match = re.search(r'var plotData2ab = eval\((.*?)\);', html, re.DOTALL)

        if match:
            data_block = match.group(1)

            # Extract all nested arrays like [Date.UTC(...), numbers...]
            array_matches = re.findall(r'\[Date\.UTC\([^\]]+\)\s*,\s*([^\]]+)\]', data_block)

            subfan_score = 0
            for arr in array_matches:
                values = [v.strip() for v in arr.split(',')]
                if len(values) > 3:
                    try:
                        subfan_score += int(values[3])  # 4th value (index 3)
                    except ValueError:
                        continue  # Skip invalid integer values

            return jsonify({"wallet_address": wallet_address, "subfan_score": subfan_score})

        else:
            return jsonify({"error": f"No 'var plotData2ab' data found for wallet {wallet_address}."}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
