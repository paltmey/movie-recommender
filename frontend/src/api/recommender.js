import axios from 'axios';

export default {
    searchMovies(query) {
        return axios.get('/search', {
            params: {
                q: query,
            },
        });
    },
    fetchPredictedMovies(idSequence) {
        return axios.post('/predict', {
            ids: idSequence,
        });
    },
};
