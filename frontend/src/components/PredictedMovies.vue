<template>
    <b-card header="Recommended movies">
        <b-card-group deck class="movie-group">
                <b-card
                    v-for="element in predictedMovies"
                    :key="element.id"
                    :img-src="element.img"
                    :img-alt="element.title"
                    img-top
                    class="movie-card"
                >
                    <b-card-text>{{element.title}} ({{element.year}})</b-card-text>
                </b-card>
        </b-card-group>
    </b-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
    components: {
    },
    computed: {
        ...mapState(['predictedMovies']),
    },
};
</script>

<style scoped>
.card-header {
    font-size: 1.3rem;
}
.movie-group {
    overflow-x: scroll;
    overflow-y: hidden;
    flex-wrap: nowrap;
}
.movie-card {
    margin-left: 4px !important;
    margin-right: 4px !important;
    min-width: 150px;
}
.movie-card .card-body {
    padding: 0.1rem;
    font-size: 0.9rem;
    font-weight: 800;
}
</style>
