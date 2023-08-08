<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container text-center">
            <div class="row">
                <div class="col-4">

                </div>
                <div class="col">
                    <br><br>
                    <p>To add Movie at Theater<br> Fill this form</p>
                    <form>
                        <div class="mb-3">
                            <label class="form-label">Select Theater</label>
                            <select class="form-select" v-model="selected_theater_id" >
                                <!-- <option selected disabled value="" >Choose Theater...</option> -->
                                <option v-for="theater in theaters" :key="theater.theater_id" :value=theater.theater_id>{{ theater.theater_name }} {{ theater.theater_place }}
                                </option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Select Movie</label>
                            <select class="form-select" v-model="selected_movie_id">
                                <!-- <option selected disabled value="">Choose Movie...</option> -->
                                <option v-for="movie in movies" :key="movie.movie_id" :value=movie.movie_id>{{ movie.movie_name }}</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <input type="number" class="form-control" v-model="ticket_price" required
                                placeholder="Ticket Price">
                        </div>
                        <div class="mb-3">
                            <input class="form-control" type="datetime-local" name="showtime" v-model="run_time">
                        </div>

                        <button type="button" class="btn btn-primary" @click="linkTheaterMovie()">Add</button>
                    </form>
                </div>
                <div class="col-4">
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios';

import refreshAccessToken from '../../../utils/refreshToken'
import AdminHeader from '../../../components/AdminHeader'

export default {
    name: 'LinkTheaterMovie',
    data() {
        return {
            movies: {},
            theaters: {},
            selected_movie_id: '',
            selected_theater_id: '',
            ticket_price: '',
            run_time: '',   // 2023-07-14T19:35         
        }
    },
    created() {
        this.allMovies()
        this.allTheaters()
    },
    methods: {
        async allMovies() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const moviesResponse = await axios.get('http://127.0.0.1:8081/api/movie')
                this.movies = moviesResponse.data
                // console.log(this.movies)
                if (this.movies.length > 0) {
                    console.log("Movie data fletch")
                }
                else {
                    console.log("No movie ceated")
                    this.$route.push('/admin/movie')

                }
            } catch (error) {
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
        async allTheaters() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersResponse = await axios.get('http://127.0.0.1:8081/api/theater')

                this.theaters = theatersResponse.data
                // console.log(this.theaters)
                if (this.theaters.length > 0) {
                    console.log("Theater data fetched")
                }
                else {
                    console.log("No theater ceated")
                    this.$route.push('/admin/theater')
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    // await this.alltheaters()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater data.')
                }
            }
        },
        async linkTheaterMovie() {
            if (!this.selected_movie_id || !this.selected_theater_id || !this.ticket_price || !this.run_time) {
                alert("All fields are required !!");
                return;
            }
            if (this.ticket_price < 0){
                alert("Ticket Price cann't be Negative ")
            }

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:8081//api/link_theater_movie/${this.selected_theater_id}/${this.selected_movie_id}`, {
                    'movie_id' : this.selected_movie_id,
                    'theater_id': this.selected_theater_id,
                    'ticket_price': this.ticket_price,
                    'timing': this.run_time,
                })
                this.$router.push("/admin/movie");
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.addMovie();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    console.log(error)
                    alert('An error occurred while creating movie')
                }

                else if (error.response && error.response.status === 409) {
                    alert(error.response.data.message)
                }
            }

        },
    },
    components: {
        'admin-header': AdminHeader
    }
}
</script>