<template>
    <b-card header-tag="header">
        <template v-slot:header>
            <b-form-input v-model="input" @keyup.enter="submit" type="search" placeholder="Search movie"></b-form-input>
        </template>

        <b-list-group class="movie-list">
            <ul class="list-unstyled">
                <draggable
                    v-model="searchResults"
                    :group="{ name: 'movies', pull: 'clone', put: false }"
                    :sort="false"
                    :move="checkMove"
                    @start="drag=true"
                    @end="drag=false"
                >
                    <b-media
                        no-body
                        class="mb-1"
                        tag="li"
                        v-for="element in searchResults"
                        :key="element.id"
                    >
                        <b-media-aside vertical-align="center">
                            <b-img :src="element.img" height="48" :alt="element.title"></b-img>
                        </b-media-aside>
                        <b-media-body class="ml-3 align-self-center">
                            <p class="mt-0 mb-1 text-left">{{element.title}} ({{element.year}})</p>
                        </b-media-body>
                    </b-media>
                </draggable>
            </ul>
        </b-list-group>
    </b-card>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import draggable from 'vuedraggable';

export default {
    components: {
        draggable,
    },
    data() {
        return {
            dragging: false,
            input: '',
        };
    },
    computed: {
        ...mapState(['searchResults', 'selectedMovies', 'maxSequenceLength']),
    },
    methods: {
        ...mapActions(['searchMovies']),
        isDuplicate(id) {
            return this.selectedMovies.some((element) => element.id === id);
        },

        checkMove(evt) {
            return this.selectedMovies.length < this.maxSequenceLength && !this.isDuplicate(evt.draggedContext.element.id);
        },
        submit() {
            this.searchMovies(this.input);
        },
    },
};
</script>

<style scoped>
.movie-list {
    height: 30vh;
    overflow: scroll;
}
</style>
