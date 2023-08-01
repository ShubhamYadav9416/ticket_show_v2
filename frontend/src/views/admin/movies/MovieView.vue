<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <br><br>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col" v-if="no_table">
                    <p><i>"No Movie is created"</i></p><br><br>
                </div>
                <div class="col" v-if="show_table">
                    <center>

                        <h5>Movies</h5>
                        <table>
                            <tr>
                                <th>Movie Id</th>
                                <th>Movie Name</th>
                                <th>Movie Tag</th>
                                <th>Movie Language</th>
                                <th>Movie Duration</th>
                                <th>Movie Description</th>
                                <th>Movie Poster</th>
                                <th>Actions</th>
                            </tr>
                            <tr v-for="movie in movies" :key="movie.movie_id">
                                <td>{{ movie.movie_id }}</td>
                                <td>{{ movie.movie_name }}</td>
                                <td>{{ movie.movie_tag }}</td>
                                <td>{{ movie.movie_language }}</td>
                                <td>{{ movie.movie_duration }}</td>
                                <td>{{ movie.movie_description.slice(0, 15) }} ...</td>
                                <td>
                                    <img :src=movie.poster_url style="max-height: 70px; max-width: 35px;">
                                </td>
                                <td><a @click="dltMovie(movie.movie_id)"><i class="bi bi-trash-fill"
                                            style="color: brown;"></i></a>/
                                    <router-link :to="`/admin/movie/edit/${movie.movie_id}`"><i class="bi bi-pencil-square"
                                            style="color: grey;"></i></router-link>
                                </td>
                            </tr>
                        </table>
                    </center>
                </div>
                <div class="col-2"></div>
            </div>
        </div><br><br>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col">
                    <div class="container text-center">
                        <div class="row">
                            <div class="col">
                                <h6>To Add New Movie</h6>
                                <router-link to="/admin/add_movie"><button>
                                        <center>+</center>
                                    </button></router-link>
                            </div>
                            <div class="col-2"></div>
                            <div class="col">
                                <h6>To Add New Movie in Theater</h6>
                                <router-link to="/admin/LinkTheaterMovie"><button>+</button></router-link>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-2">
                </div>
            </div>
        </div>
    </div>
</template>



<script>

import axios from 'axios';


import AdminHeader from '../../../components/AdminHeader'

import refreshAccessToken from '../../../utils/refreshToken'

export default {
    data() {
        return {
            movies: {},
            show_table: false,
            no_table: false,
            posterUrl: "",
            poster: "",
        }
    },
    created() {
        this.allMovies()
    },
    methods: {
        async allMovies() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const moviesResponse = await axios.get('http://127.0.0.1:8081/api/movie')
                this.movies = moviesResponse.data
                if (this.movies.length > 0) {
                    console.log("Movie data fletch")
                    this.show_table = true
                    for (let movie of this.movies){
                        this.movies[movie.movie_id - 1].poster_url = `data:image/jpeg;base64,${this.movies[movie.movie_id - 1].poster_url}`
                    }
                }
                else {
                    console.log("No movie ceated")
                    this.no_table = true
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.allMovies()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the movie data.')
                }
            }
        },
        async dltMovie(id) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.delete(`http://127.0.0.1:8081/api/movie/${id}`)
                console.log("Movie with id: " + id + " deleted")
                await this.allMovies()
            }
            catch (error) {
                console.error(error);
                alert("An error occurred while deleting movie");
            }
        },
    },
    components: {
        'admin-header': AdminHeader
    }
}
</script>


<style scoped>
.col {
    /* border: 1px solid black; */
    margin: 0;
    padding: 0;
}

button {
    background-color: rgb(165, 165, 231);
    border: 0;
    color: white;
    width: 50px;
    height: 50px;
    font-size: 25px;
    text-align: center;
    border-radius: 2rem;
}

button:hover {
    background-color: rgb(126, 126, 230);
}

table {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
    border-radius: .5em;
    margin-top: 10px;
}

th {
    background-color: rgb(128, 128, 235);
    color: white;
}

td,
th {
    padding-left: 12.5px;
    padding-right: 12.5px;
    /* border: 1px solid black; */
    font-size: small;
}

td {
    font-size: 15px;
}

tr:nth-child(even) {
    background-color: rgb(207, 231, 243);
}

tr:nth-child(odd) {
    background-color: whitesmoke;
}
</style>