import argparse
import json
import math
import os
import random
from datetime import datetime
from pathlib import Path

import tensorflow as tf
from tqdm import tqdm

DATE_FORMAT = '%Y-%m-%d'


def load_ratings(file_paths):
    print('Begin loading ratings...')

    all_user_ratings = {}
    movie_rating_counts = {}

    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as file:
            movie_id = ''

            file_name = Path(file_path).stem

            for line in tqdm(file.read().splitlines(), desc=f'Loading {file_name}...'):
                if ':' in line:
                    movie_id = line[:-1]  # remove colon

                else:
                    data = line.split(sep=',')
                    user_id = int(data[0])
                    rating = int(data[1])
                    date = datetime.strptime(data[2], DATE_FORMAT)
                    user_ratings = all_user_ratings.get(user_id, [])
                    user_ratings.append({'movie_id': movie_id, 'rating': rating, 'date': date})
                    all_user_ratings[user_id] = user_ratings

                    count = movie_rating_counts.get(movie_id, 0)
                    movie_rating_counts[movie_id] = count + 1

    return all_user_ratings, movie_rating_counts


def filter_top_movies(user_ratings, movie_rating_counts, n):
    sorted_movie_rating_counts = sorted(movie_rating_counts.items(), key=lambda item: item[1], reverse=True)
    top_movies = [item[0] for item in sorted_movie_rating_counts[:n]]
    filtered_user_ratings = {}

    for user_id, ratings in tqdm(user_ratings.items(), desc=f'Filtering top {n} movies...'):
        filtered_user_ratings[user_id] = [rating for rating in ratings if rating['movie_id'] in top_movies]

    return filtered_user_ratings, top_movies


def sort_ratings(user_ratings):
    sorted_user_ratings = {}

    for user_id, ratings in tqdm(user_ratings.items(), desc='Sorting ratings'):
        ratings.sort(key=lambda entry: entry['date'], reverse=True)
        sorted_user_ratings[user_id] = ratings

    return sorted_user_ratings


def load_movie_titles(movie_titles_path):
    print('Reading movie titles...')

    movie_titles = {}

    with open(movie_titles_path, encoding='ISO-8859-1') as file:
        for line in file.readlines():
            id, year, title = line.strip().split(sep=',', maxsplit=2)
            movie_titles[id] = {'title': title, 'year': year}

    return movie_titles


def build_vocab(movies, movie_titles_path):
    movie_titles = load_movie_titles(movie_titles_path)

    return {id: {'id': i, 'title': movie_titles[id]['title'], 'year': movie_titles[id]['year']} for i, id in
            enumerate(sorted(movies))}


def get_chunks(lst, chunksize):
    return [lst[i:i + chunksize] for i in range(0, len(lst), chunksize)]


def generate_label_and_sequences(data):
    labels = []
    sequences = []

    for sequence in data:
        if len(sequence) > 1:
            labels.append(sequence[0])
            sequences.append(sequence[1:])

    return sequences, [labels]


def transform_data(data, vocab):
    sequences = []
    for sequence in data:
        sequences.append([vocab[entry['movie_id']]['id'] for entry in sequence])

    return sequences


def generate_rating_sequences(user_ratings, vocab, chunksize, min_ratings):
    sequences = []
    labels = []
    for user_id, ratings in tqdm(user_ratings.items(), desc='Generating chunks...'):
        if len(ratings) >= min_ratings:
            chunks = get_chunks(ratings, chunksize + 1)
            generated_sequences, generated_labels = generate_label_and_sequences(chunks)
            transformed_sequences = transform_data(generated_sequences, vocab)
            transformed_labels = transform_data(generated_labels, vocab)
            sequences.extend(transformed_sequences)
            labels.extend(transformed_labels[0])

    return sequences, labels


def get_train_test_indices(data_length, split_percentage):
    random_indices = random.sample(range(data_length), data_length)
    train_len, test_len = math.floor(data_length * (1 - split_percentage)), math.floor(data_length * split_percentage)
    train_indices, test_indices = random_indices[:train_len - 1], random_indices[train_len:]

    return train_indices, test_indices


def generate_train_test_split(sequences, labels, split_percentage):
    data_length = len(labels)
    train_indices, test_indices = get_train_test_indices(data_length, split_percentage)

    train_sequences = [sequences[index] for index in train_indices]
    train_labels = [labels[index] for index in train_indices]

    test_sequences = [sequences[index] for index in test_indices]
    test_labels = [labels[index] for index in test_indices]

    return train_sequences, train_labels, test_sequences, test_labels


def _int_feature(list_of_ints):  # int64
    return tf.train.Feature(int64_list=tf.train.Int64List(value=list_of_ints))


def to_tfrecord(sequence, label):
    feature = {
        'rating_chunk': _int_feature(sequence),  # one image in the list
        'label': _int_feature([label]),  # one class in the list
    }
    return tf.train.Example(features=tf.train.Features(feature=feature))


def write_tfrecord_shards(sequences, labels, filename, output_path, shard_size):
    shard_ranges = get_chunks(range(len(labels)), shard_size)

    for shard_index, shard_range in tqdm(enumerate(shard_ranges), total=len(shard_ranges), desc='Writing shards...'):
        exact_shard_size = len(shard_range)
        shard_filename = os.path.join(output_path, f'{filename}_{shard_index}_{exact_shard_size}.tfrec')

        with tf.io.TFRecordWriter(shard_filename) as out_file:
            for index in shard_range:
                example = to_tfrecord(sequences[index], labels[index])
                out_file.write(example.SerializeToString())

            print("Wrote file {} containing {} records".format(shard_filename, exact_shard_size))


def write_vocab(vocab, filename, output_path):
    print('Writing vocab...')

    with open(Path(output_path).joinpath(filename), 'w') as file:
        json.dump(vocab, file)


def generate_dataset(netflix_prize_data_dir, dataset_name, output_path, top_movie_n, chunksize, min_ratings,
                     split_percentage, shard_size, generate_check_dataset, check_dataset_cutoff):
    netflix_prize_data_path = Path(netflix_prize_data_dir)

    ratings, movie_ratings_count = load_ratings([netflix_prize_data_path.joinpath('combined_data_1.txt'),
                                                 netflix_prize_data_path.joinpath('combined_data_2.txt'),
                                                 netflix_prize_data_path.joinpath('combined_data_3.txt'),
                                                 netflix_prize_data_path.joinpath('combined_data_4.txt')])

    filtered_ratings, top_movies = filter_top_movies(ratings, movie_ratings_count, n=top_movie_n)
    sorted_ratings = sort_ratings(filtered_ratings)
    vocab = build_vocab(top_movies, netflix_prize_data_path.joinpath('movie_titles.csv'))
    sequences, labels = generate_rating_sequences(sorted_ratings, vocab, chunksize, min_ratings)
    train_sequences, train_labels, test_sequences, test_labels = generate_train_test_split(sequences, labels,
                                                                                           split_percentage)

    Path(output_path).mkdir(parents=True, exist_ok=True)

    print('Writing train shards...')
    write_tfrecord_shards(train_sequences, train_labels, f'{dataset_name}_{chunksize}_train', output_path, shard_size)
    print('Writing test shards...')
    write_tfrecord_shards(test_sequences, test_labels, f'{dataset_name}_{chunksize}_test', output_path, shard_size)

    if generate_check_dataset:
        print('Writing check shards...')
        write_tfrecord_shards(test_sequences[:check_dataset_cutoff], test_labels[:check_dataset_cutoff],
                              f'{dataset_name}_check', output_path, shard_size)

    write_vocab(vocab, f'{dataset_name}_vocab.json', output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script to generate a tf record dataset for the netflix prize dataset.')
    parser.add_argument('--netflix_prize_data_dir', type=str, default='data/raw/netflix-prize-data')
    parser.add_argument('--dataset_name', type=str, default='netflix')
    parser.add_argument('--output_path', type=str, default='data/processed/netflix')
    parser.add_argument('--top_movie_n', type=int, default=500)
    parser.add_argument('--chunksize', type=int, default=5)
    parser.add_argument('--min_ratings', type=int, default=0)
    parser.add_argument('--split_percentage', type=float, default=0.2)
    parser.add_argument('--shard_size', type=int, default=650000)
    parser.add_argument('--generate_check_dataset', action='store_true')
    parser.add_argument('--check_dataset_cutoff', type=int, default=1000)

    args = parser.parse_args()

    output_path = args.output_path if args.output_path else args.dataset_name
    min_ratings = args.min_ratings if args.min_ratings > 0 else args.chunksize

    generate_dataset(args.netflix_prize_data_dir, args.dataset_name, output_path, args.top_movie_n, args.chunksize,
                     min_ratings, args.split_percentage, args.shard_size, args.generate_check_dataset,
                     args.check_dataset_cutoff)
