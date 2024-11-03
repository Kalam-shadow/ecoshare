from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Download 'punkt' tokenizer from NLTK
nltk.download('punkt_tab')

# Function to load the language model for zero-shot classification
def load_language_model():
    try:
        # Try loading the larger model
        print("Loading facebook/bart-large-mnli model...")
        return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1)  # CPU only
    except Exception as e:
        print(f"Failed to load facebook/bart-large-mnli model. Error: {e}")
        print("Loading a smaller fallback model: valhalla/distilbart-mnli-12-1...")
        return pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", device=-1)  # CPU only

# Initialize the pipeline
language_model = load_language_model()

# Sample categories in multiple languages or varied terms
categories = {
    "food": ["food", "groceries", "meal", "nourishment", "alimentation"],
    "clothing": ["clothes", "garments", "apparel", "wearing", "outfit", "attire"]
}

# Function to standardize category name using NLP
def categorize_item(item):
    labels = ["food", "clothing"]
    result = language_model(item, labels)
    return result['labels'][0]  # The most likely category

# Example to match category names across different languages or variations
def preprocess_text(text):
    # Tokenization using NLTK's 'punkt' tokenizer
    tokens = nltk.word_tokenize(text.lower())
    return " ".join(tokens)

# Function to match people based on categories
def match_categories(seller_items, buyer_needs):
    # Preprocess both seller items and buyer needs
    seller_items = [preprocess_text(item) for item in seller_items]
    buyer_needs = [preprocess_text(need) for need in buyer_needs]
    
    # Categorize both the items
    seller_categories = [categorize_item(item) for item in seller_items]
    buyer_categories = [categorize_item(need) for need in buyer_needs]
    
    # Perform matching based on categories
    matches = []
    for i, seller_category in enumerate(seller_categories):
        for j, buyer_category in enumerate(buyer_categories):
            if seller_category == buyer_category:
                matches.append((seller_items[i], buyer_needs[j], seller_category))
    
    return matches

# Example sellers and buyers
sellers = ["shirts and pants", "bread and milk", "fruits and vegetables"]
buyers = ["I need some clothes", "I'm looking for groceries", "I want to buy a jacket"]

# Find matches between sellers and buyers
matches = match_categories(sellers, buyers)

# Display matches
for match in matches:
    seller, buyer, category = match
    print(f"Seller: {seller} | Buyer: {buyer} | Matched Category: {category}")
