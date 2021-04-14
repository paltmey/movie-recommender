const movies = [
    {
        id: 0,
        title: 'The Matrix',
        year: 1999,
        img:
            'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
    },
    {
        id: 1,
        title: 'Inception',
        year: 2010,
        img:
            'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_UX182_CR0,0,182,268_AL_.jpg',
    },
    {
        id: 2,
        title: 'Fight Club',
        year: 1999,
        img:
            'https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX182_CR0,0,182,268_AL_.jpg',
    },
    {
        id: 3,
        title: 'The Lord of The Rings: The Fellowship of the Ring',
        year: 2001,
        img:
            'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_UX182_CR0,0,182,268_AL_.jpg',
    },
    {
        id: 4,
        title: 'Forrest Gump',
        year: 1994,
        img:
            'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY268_CR1,0,182,268_AL_.jpg',
    },
];

export default {
    searchMovies() {
        return new Promise((resolve) => {
            setTimeout(() => resolve(movies), 1000);
        });
    },
    getPredictedMovies() {
        return new Promise((resolve) => {
            setTimeout(() => resolve(movies), 1000);
        });
    },
};
