import Vue from 'vue';
import Vuex from 'vuex';

import api from '../api/recommender';

Vue.use(Vuex);

// const arrayEquals = (a, b) => a.length === b.length && a.every((element, index) => element === b[index]);

export default new Vuex.Store({
    state: {
        selectedMovies: [],
        lastIdSequence: [],
        searchResults: [],
        predictedMovies: [],
        maxSequenceLength: 15,
    },
    mutations: {
        setSelectedMovies(state, selectedMovies) {
            Vue.set(state, 'selectedMovies', selectedMovies);
        },
        setSearchResults(state, searchResults) {
            Vue.set(state, 'searchResults', searchResults);
        },
        setPredictedMovies(state, predictedMovies) {
            Vue.set(state, 'predictedMovies', predictedMovies);
        },
    },
    actions: {
        searchMovies({ commit }, query) {
            api.searchMovies(query).then((result) => {
                commit('setSearchResults', result.data);
            });
        },
        getPredictedMovies({ commit, state }) {
            if (state.selectedMovies.length > 0) {
                const idSequence = state.selectedMovies.map((element) => element.id);

                api.fetchPredictedMovies(idSequence).then((result) => {
                    commit('setPredictedMovies', result.data);
                });
            } else {
                commit('setPredictedMovies', []);
            }
        },
        setSelectedMovies({ commit, dispatch }, selectedMovies) {
            commit('setSelectedMovies', selectedMovies);
            dispatch('getPredictedMovies');
        },
    },
    modules: {},
});
