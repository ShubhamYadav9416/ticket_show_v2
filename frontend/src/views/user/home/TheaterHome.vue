<template>
    <div class="card" style="width: 18rem;">
        <img src="../../../assets/default_theater.jpg" class="card-img-top" alt="Theater image">
        <div class="card-body">
            <h5 class="card-title">{{ theater.theater_name }}</h5>
            <p class="location"><i class="bi bi-geo-alt-fill" style="color:green"></i>{{ theater.theater_place }}, {{
                theater.theater_location }}
            </p>
            <p style="font-size: 12px; margin-top: -15px;"><i class="bi bi-star-fill" style="color: red;"></i> 2.2/5 25
                Votes</p>
            <form class="d-flex" role="search">
                <input class="form-control me-2" type="number" placeholder="1 to 5" aria-label="Search"
                    style="width: 60%; height: 30px;" v-model="rate">
                <button class="btn btn-outline-success" type="button" style="height: 30px; padding-top: 2px;" @click="rateTheater()">
                    <p>Rate<i class="bi bi-star" style="color: rgb(235, 183, 183);"></i></p>
                </button>
            </form>
        </div>
        <ul class="list-group list-group-flush">
            <li class="list-group-item">Currently Showing</li>
            <div v-for="movie in theater.movies" :key="movie.theater_movie_id">
                <li class="list-group-item"><span class="movie_name">{{ movie.movie_name }}<i class="movie_tag">{{
                    movie.movie_tag }}</i></span>
                    <span v-show="!movie.housefull"><router-link :to="`/movie/booking/${movie.theater_movie_id}`">
                            <button type="button" class="btn btn-outline-primary" style="">Book</button>
                        </router-link></span>
                    <span v-show="movie.housefull">
                        <button type="button" class="btn btn-outline-danger" disabled
                            style="font-size: 10px;">HouseFull</button>
                    </span>
                </li>
            </div>
        </ul>
    </div>
</template>


<script>
import axios from 'axios'
import refreshAccessToken from '@/utils/refreshToken'

export default {
    name: 'TheaterHome',
    props: ['theater'],
    data() {
        return {
            show_rate_form : false,
            rate : "",
        }
    },
    created() {
        this.theateruserRatings(),
        this.theaterRatings(),
    },
    methods: {
        async theateruserRatings() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersRatingResponse = await axios.get(`http://127.0.0.1:8081/api/user/rating/theater/${this.theater.theater_id}`)

                if (theatersRatingResponse.data.staus === "not_rated"){
                    this.show_rate_form = true
                }
                else{
                    this.theater_rating = theatersRatingResponse.data.rating
                    this.show_rate_form = false
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.theateruserRatings()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater user rating data.')
                }
            }
        },
            async rateTheater() {
                if (!this.rate || this.rate > 6 || this.rate < 1 ) {
                    alert("Rate theater between 1 to 5 !!");
                    return;
                }
            
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post(`http://127.0.0.1:8081/api/user/rating/theater/${this.theater.theater_id}`, {
                    rating: this.rate,
                })
                this.theateruserRatings()
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.rateTheater();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    alert('An error occurred while creating theater.')
                }
            }

        },
        async theaterRatings(){
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersRatingResponse = await axios.get(`http://127.0.0.1:8081/api/rating/theater/${this.theater.theater_id}`)

                if (theatersRatingResponse.data.staus === "not_rated"){
                    this.show_rate_form = true
                }
                else{
                    this.theater_rating = theatersRatingResponse.data.rating
                    this.show_rate_form = false
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.theateruserRatings()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater user rating data.')
                }
            }
        }
    }
}

</script>

<style scoped>
.location {
    font-size: small;
}

.movie_name {
    font-weight: 700;
}

.movie_tag {
    font-weight: 200;
    font-size: small;
    margin: 0 20px 0 10px;
}</style>