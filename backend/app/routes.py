from flask import Blueprint, jsonify, request
from .utils import analyze_articles

sentiment_bp = Blueprint('sentiment', __name__)
@sentiment_bp.route('/analyze', methods=['GET'])
def analyze():
    ticker = request.args.get('ticker', 'AAPL')
    try:
        results = analyze_articles(ticker)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500