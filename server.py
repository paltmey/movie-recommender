import json
import pymongo
import numpy as np
import tensorflow as tf

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

MAX_SEQ_LENGTH = 15
K = 10

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:32768/movielens'  # configure MongoDB connection
mongo = PyMongo(app)

vocab_path = 'movielens/movielens_vocab.json'
with open(vocab_path) as file:
    vocab = json.load(file)

model = tf.keras.models.load_model('models/model_movielens.h5')


def predict(id_sequence, model, k):
    id_sequence = [int(id) for id in id_sequence]
    paddings = [[0, 0], [0, MAX_SEQ_LENGTH - len(id_sequence)]]

    input_chunk = tf.pad(tf.reshape(id_sequence, (1, -1)), paddings, 'CONSTANT')
    probs = model.predict(input_chunk)
    predicted_ids = tf.argsort(probs, direction='DESCENDING')[0][:k+len(id_sequence)]
    predicted_ids = [int(id) for id in predicted_ids]  #
    predicted_ids = [id for id in predicted_ids if id-1 not in set(id_sequence)][:k]  # remove query ids from prediction
    probs = probs[0][np.array(predicted_ids)]
    predicted_ids = [str(id-1) for id in predicted_ids]
    return predicted_ids, probs


def set_img_size(img_url, size):
    return f'{img_url[:-4]}._V1_SY{size}.jpg'


def format_prob(prob):
    return f"{prob*100:.2f}"


@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('q')
    results = (mongo.db.movielens
               .find({'$text': {'$search': query}}, {'score': {'$meta': 'textScore'}})
               .sort('textScore', pymongo.DESCENDING)
               )
    view_model = [{'id': movie['id'], 'title': movie['title'], 'year': movie['year'], 'img': set_img_size(movie['img'], 48)} for movie in
                  results]
    return jsonify(view_model)


@app.route('/predict', methods=['POST'])
def predict_movies():
    ids = request.json['ids']
    predicted_ids, probs = predict(ids, model, K)

    pipeline = [
        {'$match': {'id': {'$in': predicted_ids}}},
        {'$addFields': {'__order': {'$indexOfArray': [predicted_ids, "$id"]}}},
        {'$sort': {'__order': 1}}
    ]
    results = mongo.db.movielens.aggregate(pipeline)
    view_model = [{'id': movie['id'], 'title': movie['title'], 'prob':format_prob(probs[index]), 'year': movie['year'], 'img': set_img_size(movie['img'], 300)} for index, movie in
                  enumerate(results)]
    return jsonify(view_model)


if __name__ == '__main__':
    app.run(debug=True)
