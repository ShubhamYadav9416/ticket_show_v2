<template>
    <div class="container text-center">
        <div class="row">
            <div class="col-2">
                <router-link to="/home">Return to Home Page</router-link>
            </div>
            <div class="col">
                <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search for Movie, Theater, place..."
                        v-model=search_input aria-label="Search">
                </form>
                <h5 style="margin: 10px;" v-show="search_input">Results</h5>
                <div>
                    <div class="list-group" v-show="search_input">
                        <a href="#" @click="filter_by_movie(movie_filter.movie_id)"
                            class="list-group-item list-group-item-action" style="padding-bottom: 0px;"
                            v-for="movie_filter in movie_filters" :key="movie_filter.id"
                            v-show="movie_filter.movie_name.includes(search_input)">
                            <p align="left" style="position: fixed; margin-left: 100px;"><i class="bi bi-film"></i></p>{{
                                movie_filter.movie_name }}
                        </a>
                        <a href="#" @click="filter_by_theater(theater_filter.theater_id)"
                            class="list-group-item list-group-item-action" style="padding-bottom: 0px;"
                            v-for="theater_filter in theater_filters" :key="theater_filter.id"
                            v-show="theater_filter.theater_name.includes(search_input)">
                            <p align="left" style="position: fixed; margin-left: 100px;"><i class="bi bi-building"></i></p>
                            {{ theater_filter.theater_name }}
                        </a>
                        <a href="#" @click="filter_by_theater(place_filter.theater_id)"
                            class="list-group-item list-group-item-action" style="padding-bottom: 0px;"
                            v-for="place_filter in place_filters" :key="place_filter.id"
                            v-show="place_filter.theater_place.includes(search_input)">
                            <p align="left" style="position: fixed; margin-left: 100px;"><i class="bi bi-geo-alt"></i></p>{{
                                place_filter.theater_place }}
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-2">

            </div>
        </div>
    </div>
</template>


<script>

import axios from 'axios'
import refreshAccessToken from '@/utils/refreshToken'

export default {
    name: 'userSearch',
    data() {
        return {
            search_input: "",
            str: "hello",
            movie_filters: [],
            theater_filters: [],
            place_filters: []
        }
    },
    created() {
        this.allFilters()
    },
    methods: {
        async allFilters() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const allFiltersResponse = await axios.get(`http://127.0.0.1:8081/api/search/filters`)
                console.log(allFiltersResponse)
                this.movie_filters = allFiltersResponse.data.movie
                this.theater_filters = allFiltersResponse.data.theater
                this.place_filters = allFiltersResponse.data.place
                console.log(this.movie_filters)
                console.log(this.theater_filterfilter_by_movies)
                console.log(this.place_filters)
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.allFilters()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching filters')
                }
            }
        },
        async filter_by_movie(id) {

            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const allTheaterMovieResponse = await axios.get(`http://127.0.0.1:8081/api/search/movie/${id}`)
                console.log(allTheaterMovieResponse)
                this.$router.push({
                    name: 'search-result',
                    query : {
                        allTheaterMovieResponse
                    }
                })
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.filter_by_movie(id)
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while searching movie')
                }
            }
        },
        async filter_by_theater(id) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const allTheaterMovieResponse = await axios.get(`http://127.0.0.1:8081/api/search/theater/${id}`)
                console.log(allTheaterMovieResponse)
                this.$router.push({
                    name: 'search-result',
                    query : {
                        allTheaterMovieResponse
                    }
                })
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.filter_by_theater(id)
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while searching theater')
                }
            }
        }
    }
}


</script>


<style scoped>
.col {
    border: 1px solid black;
    margin-top: 50px;
    padding: 20px;
}
</style>