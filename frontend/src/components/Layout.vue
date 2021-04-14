<template>
    <b-container>
        <b-row>
            <b-col cols="6" class="panel">
                <MovieList />
            </b-col>
            <b-col cols="6" class="panel">
                <SelectedMovies />
            </b-col>
        </b-row>
        <b-row>
            <b-col class="panel bottom-panel">
                <PredictedMovies />
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import MovieList from './MovieList.vue';
import SelectedMovies from './SelectedMovies.vue';
import PredictedMovies from './PredictedMovies.vue';

export default {
    name: 'Layout',
    components: {
        SelectedMovies,
        MovieList,
        PredictedMovies,
    },
};
</script>

<style scoped>
.panel {
    padding-left: 8px;
    padding-right: 8px;
}
.bottom-panel {
    margin-top: 16px;
}
</style>
