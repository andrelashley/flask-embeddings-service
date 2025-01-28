from flask import Flask, render_template, jsonify
from models import db, Item
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)

# Configure PostgreSQL database URI


# Initialize SQLAlchemy with the Flask app
db.init_app(app)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [
        {
            "ItemId": item.ItemId,
            "Text": item.Text,
            "Embedding": item.Embedding
        }
        for item in items
    ]
    return jsonify(items_list)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    # Fetch the item by ID
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    
    # Convert the item to a dictionary
    item_data = {
        "ItemId": item.ItemId,
        "Text": item.Text,
        "Embedding": item.Embedding
    }
    return jsonify(item_data)

@app.route('/api/items/embedding/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Fetch the item by ID
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found"}), 404
    
    embedding = model.encode(item.Text)   
    embedding_list = embedding.tolist()

    return jsonify({"embedding": embedding_list})
