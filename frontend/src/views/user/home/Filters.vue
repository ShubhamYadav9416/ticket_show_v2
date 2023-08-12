<template>
    <div class="filters">
        <h3>Filters</h3>
        <div class="filter_rating">
            <dt>Filter by rating</dt>
            <dd @click="filter_by_rate(4)"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i
                    class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star"></i>
            </dd>
            <dd @click="filter_by_rate(3)"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i
                    class="bi bi-star-fill"></i><i class="bi bi-star"></i><i class="bi bi-star"></i></dd>
            <dd @click="filter_by_rate(2)"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i
                    class="bi bi-star"></i><i class="bi bi-star"></i><i class="bi bi-star"></i></dd>
            <dd @click="filter_by_rate(1)"><i class="bi bi-star-fill"></i><i class="bi bi-star"></i><i
                    class="bi bi-star"></i><i class="bi bi-star"></i><i class="bi bi-star"></i></dd>
        </div>
    </div>
</template>

<script>

import axios from 'axios';
import refreshAccessToken from '@/utils/refreshToken';


export default {
    name: 'userFilters',
    props: {
        theater_movies_for_filters: Array,
    },
    data() {
        return {
            filtered_theaters: [],
        }
    },
    methods: {
        async filter_by_rate(value) {
            console.log(value)
            this.filtered_theaters = []
            for (let theater_movie of this.theater_movies_for_filters) {
                try {
                    let access_token = localStorage.getItem('access_token')

                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                    const theatersRatingResponse = await axios.get(`http://127.0.0.1:8081/api/rating/theater/${theater_movie.theater_id}`)

                    if (theatersRatingResponse.data.votes === 0) {
                        continue
                    }
                    else {
                        const theater_cal_rating = theatersRatingResponse.data.total_rating / theatersRatingResponse.data.votes
                        if (theater_cal_rating >= value && theater_cal_rating < value + 1) {
                            this.filtered_theaters.push(theater_movie)
                        }
                    }
                }
                catch (error) {
                    if (error.response && error.response.status === 401) {
                        await refreshAccessToken()
                        await this.theaterRatings()
                    }

                    else if (error.response) {
                        console.error(error)
                        alert('An error occurred while fetching the theater user rating data.')
                    }
                }
            }
            const allTheaterMovieResponse = this.filtered_theaters
            // console.log(theater_movies_filtered)
            this.$router.push({
                    name: 'search-result',
                    query : {
                        allTheaterMovieResponse,
                        filter_results: true,
                        search_results: false
                    }
                })

        }
    }
}

</script>

<style scoped>
.filters {
    margin-top: 150px;
}

.filters h3 {
    font-size: 20px;
}

.filters dt {
    font-size: 15px;
    font-weight: 300;
}

.filters dd {
    color: rgb(232, 129, 129);
    margin-bottom: -5px;
}

.filter_tags {
    margin-top: 15px;
}

.filter_tags dd {
    color: rgb(54, 52, 52);
    font-weight: 300;
    font-size: 14px;
}

.filter_tags dd:hover {
    color: black;
    font-size: 16px;
}

.filter_rating dd:hover {
    color: red;
    font-size: 18px;
}
</style>