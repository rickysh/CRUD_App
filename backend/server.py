from bson.objectid import ObjectId
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient


template_dir = "../frontend/templates"

app = Flask(__name__, template_folder=template_dir)

# MongoDB connection
client = MongoClient('mongodb+srv://<username>:<password>@cluster0.kuewrfz.mongodb.net/')
db = client['full_stack_db']  # Replace 'your_database_name' with your actual database name
collection = db['full_stack_col_2']  # Replace 'your_collection_name' with your actual collection name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Retrieve entries from MongoDB collection
        num_records = collection.count_documents({})
        records = collection.find()
        return render_template('index.html', num_records=num_records, records=records)
    
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = int(request.form['age'])
        city = request.form['city']
        email = request.form['email']
        # Create new document dictionary
        new_doc = {
            'name': name,
            'age': age,
            'city': city,
            'email': email
        }
        # Insert new entry into MongoDB collection
        collection.insert_one(new_doc)
        return redirect(url_for('index'))
    
@app.route('/delete/<_id>', methods=['POST'])
def delete(_id):
    collection.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('index'))

@app.route('/update/<_id>', methods=['POST'])
def update(_id):
    if request.method == 'POST':
        # Get form data
        update_name = request.form['update_name']
        update_age = int(request.form['update_age'])  # Ensure age is converted to int
        update_city = request.form['update_city']
        update_email = request.form['update_email']
        # Create new document dictionary
        update_doc = {
            'name': update_name,
            'age': update_age,
            'city': update_city,
            'email': update_email
        }
        collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': update_doc}
        )
        return redirect(url_for('index'))  # Redirect to homepage after updating entry

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
