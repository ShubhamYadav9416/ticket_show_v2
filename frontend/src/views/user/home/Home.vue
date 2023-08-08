<template>
    <div>
        <user-header></user-header>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2">
                    <!-- <filters></filters> -->
                </div>
                <div class="col-10">
                    <div class="container text-center" v-show="display">
                        <div class="row" id="display_row">
                            <div class="col center-block" v-for="theater_movie in theater_movies"
                                :key="theater_movie.theater_id">
                                <theater-view style="margin-bottom: 20px;" :theater="theater_movie"></theater-view>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserHeaderVue from '@/components/UserHeader.vue';
// import Filters from './Filters.vue';
import TheaterHome from './TheaterHome.vue';

import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';

export default {
    name: 'UserHome',
    data() {
        return {
            theater_movies: {},
            display: false,
        }
    },
    components: {
        'user-header': UserHeaderVue,
        // 'filters': Filters,
        'theater-view': TheaterHome,
    },
    created() {
        this.allHomeTheaterMovies()
    },
    methods: {
        async allHomeTheaterMovies() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersResponse = await axios.get('http://127.0.0.1:8081/api/movies_at_theater/home')

                this.theater_movies = theatersResponse.data
                if (this.theater_movies.length > 0) {
                    console.log("Theaters data fetched")
                    this.display = true
                }
                else {
                    console.log("No theater ceated")
                    this.display = false
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.allHomeTheaterMovies()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater data.')
                }
            }
        },
    }
}

</script>

<style scoped>
.col-2 {
    margin: 0;
    padding: 0;
}


.view_p {
    margin-bottom: 0px;
    margin-top: 10px;
    font-weight: 100;
    font-size: 10px
}

button {
    margin-top: 0px;
    color: rgb(202, 209, 235);
    border: none;
    font-size: 15px;
}

button:hover {
    background-color: rgb(159, 182, 242);
}

#space {
    height: 50px;
}

#display_row {
    margin: 50px 30px 10px 30px;
}
</style>