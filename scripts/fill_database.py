import argparse
import json

from pymongo import MongoClient


def fill_db(imdb_data_path, host, port):
    with open(imdb_data_path) as file:
        imdb_data = json.load(file)

    transformed_data = []
    for id, entry in imdb_data.items():
        transformed_data.append({'id': id, **entry})

    client = MongoClient(host, port)
    db = client.movielens
    db_collection = db.movielens
    db_collection.insert_many(transformed_data)

    db_collection.create_index('id')
    db_collection.create_index([('title', 'text')])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script to featch IMDB data for a dataset.')
    parser.add_argument('--imdb_data_path', type=str, default='data/processed/movielens/imdb_data.json')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=32768)

    args = parser.parse_args()
    fill_db(args.imdb_data_path, args.host, args.port)
