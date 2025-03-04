from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

@app.route('/products')
def get_products():
    cache = redis_client.get('products')
    if cache:
        return jsonify({'source': 'cache', 'data': cache})
    
    # Simulate DB call
    products = [{'id': 1, 'name': 'Product 1'}, {'id': 2, 'name': 'Product 2'}]
    redis_client.setex('products', 30, str(products))
    return jsonify({'source': 'database', 'data': products})

# Add a health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)