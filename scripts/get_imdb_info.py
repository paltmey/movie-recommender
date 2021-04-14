import argparse
import json
from imdb import IMDb
from tqdm import tqdm


def fetch_imdb_info(vocab_path, output_path):
    print('Reading vocab...')
    with open(vocab_path) as file:
        vocab = json.load(file)

    ia = IMDb()

    imdb_info = {}
    for id, entry in tqdm(vocab.items(), desc='Fetching IMDb info...'):
        imdb_id = entry['imdb']

        try:
            movie = ia.get_movie(imdb_id)
            imdb_info[id] = {'imdb': imdb_id, 'title': movie['title'], 'year': movie['year'],
                             'img': movie['full-size cover url'], 'rating': movie['rating']}
        except:
            print(f'Error. Fetched info for {len(imdb_info)} movies. Last id: {id}.')

            with open(output_path + '.tmp', 'w') as file:
                json.dump(imdb_info, file)

    print(f'Finished fetching info for {len(imdb_info)} movies.')

    with open(output_path, 'w') as file:
        json.dump(imdb_info, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script to featch IMDB data for a dataset.')
    parser.add_argument('--vocab_path', type=str, default='data/processed/movielens/movielens_vocab.json')
    parser.add_argument('--output_path', type=str, default='data/processed/movielens/imdb_data.json')


    args = parser.parse_args()
    fetch_imdb_info(args.vocab_path, args.output_path)
