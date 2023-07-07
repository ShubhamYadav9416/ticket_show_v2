<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col">
                    <div class="container text-center">
                        <div class="row">
                            <div class="col"></div>
                            <div class="col-2">
                                hello
                            </div>
                            <div class="col"></div>
                        </div>
                    </div>
                </div>
                <div class="col-2"> </div>
            </div>
        </div>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col" v-if="no_table">
                    <br>
                    <p>No Table is created</p>
                </div>
                <div class="col" v-if="show_table">
                    <br>
                    <h2>Movies</h2>
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
                            <td>{{ movie.id }}</td>
                            <td>{{ movie.movie_name }}</td>
                            <td>{{ movie.movie_tag }}</td>
                            <td>{{ movie.movie_language }}</td>
                            <td>{{ movie.movie_duration }}</td>
                            <td>{{ movie.movie_description }} ...</td>
                            <td><a href="movie.movie_image_path">view</a></td>
                            <td><a href="#"><i class="bi bi-trash-fill" style="color: brown;"></i></a>/<a href="#"><i
                                        class="bi bi-pencil-square" style="color: grey;"></i></a></td>
                        </tr>
                    </table>
                </div>
                <div class="col-2"></div>
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
        }
    },
    created() {
        this.allMovies()
    },
    methods: {
        async allMovies() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer' + access_token

                const moviesResponse = await axios.get('http://127.0.0.1:8081/api/movie')

                this.movies = moviesResponse.data
                if (this.movies.length > 0) {
                    console.log("Movie data fletch")
                    this.show_table = true
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
                    alert('An error occurred while fetching the followers data.')
                }
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
    border: 1px solid black;
    margin: 0;
    padding: 0;
}

table {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
    border-radius: .5em;
    margin-top: 10px;
}

th {
    background-color: darkblue;
    color: white;
}

td,
th {
    padding-left: 12.5px;
    padding-right: 12.5px;
    /* border: 1px solid black; */
}

td {
    font-size: 15px;
}

tr:nth-child(even) {
    background-color: rgb(131, 202, 237);
}

tr:nth-child(odd) {
    background-color: whitesmoke;
}
</style>