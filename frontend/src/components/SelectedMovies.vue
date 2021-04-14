<template>
    <b-card header="Selected movies">
        <b-list-group flush class="movie-list" ref="sortableList">
            <draggable
                v-model="selectedMovies"
                class="drag-area"
                group="movies"
                ghost-class="ghost"
                animation="200"
                @start="drag = true"
                @end="onEnd"
            >
                <b-media
                    no-body
                    class="mb-1"
                    tag="li"
                    v-for="element in selectedMovies"
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
        </b-list-group>
    </b-card>
</template>

<script>
import { mapActions } from 'vuex';
import draggable from 'vuedraggable';

export default {
    components: {
        draggable,
    },
    data() {
        return {
            enabled: true,
            drag: false,
        };
    },
    computed: {
        selectedMovies: {
            get() {
                return this.$store.state.selectedMovies;
            },
            set(value) {
                this.setSelectedMovies(value);
            },
        },
    },
    methods: {
        ...mapActions(['setSelectedMovies', 'getPredictedMovies']),
        onEnd(evt) {
            this.$data.drag = false;

            const target = document.elementFromPoint(
                evt.originalEvent.clientX,
                evt.originalEvent.clientY,
            );

            if (!this.$refs.sortableList.contains(target)) {
                this.setSelectedMovies(this.selectedMovies.filter((_, index) => index !== evt.oldIndex));
            }
        },
    },
};
</script>

<style scoped>
.ghost {
    opacity: 0.5;
    background: #f8f8f8;
}
.list-group-item {
    cursor: move;
}
.movie-list {
    height: 30vh;
    overflow: scroll;
}
.card-header {
    height: 63px;
    font-size: 1.3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

</style>
