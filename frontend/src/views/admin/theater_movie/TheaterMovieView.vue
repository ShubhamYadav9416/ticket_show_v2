<template>
    <div id="outer_div">

        <br><br>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col" v-if="table">
                    <div v-if="running_table">
                        <center>

                            <h5>Movies Booking Running</h5>
                            <table>
                                <tr>
                                    <th>Theater Movie Id</th>
                                    <th>Theater Name</th>
                                    <th>Movie Name</th>
                                    <th>Ticket Price</th>
                                    <th>Show Date</th>
                                    <th>Show Timing</th>
                                    <th>Actions</th>
                                </tr>
                                <tr v-for="item in runningBooking" :key="item.id">
                                    <td>{{ item.theater_movie_id }}</td>
                                    <td>{{ item.theater_name }}</td>
                                    <td>{{ item.movie_name }}</td>
                                    <td>{{ item.ticket_price }}</td>
                                    <td>{{ ((new Date(item.timing)).toString()).slice(0, 16) }}</td>
                                    <td>{{ ((new Date(item.timing)).toString()).slice(16, 21) }}</td>
                                    <td><a @click="dltTheaterMovie(item.theater_movie_id)"><i class="bi bi-trash-fill"
                                                style="color: brown;"></i></a></td>
                                </tr>
                            </table>
                        </center>
                    </div>
                    <div v-if="stoped_table">
                        <center>

                            <h5>Movies Booking Stoped</h5>
                            <table>
                                <tr>
                                    <th>Theater Movie Id</th>
                                    <th>Theater Name</th>
                                    <th>Movie Name</th>
                                    <th>Ticket Price</th>
                                    <th>Show Date</th>
                                    <th>Show Timing</th>
                                    <th>Actions</th>
                                </tr>
                                <tr v-for="item in stopedBooking" :key="item.id">
                                    <td>{{ item.theater_movie_id }}</td>
                                    <td>{{ item.theater_name }}</td>
                                    <td>{{ item.movie_name }}</td>
                                    <td>{{ item.ticket_price }}</td>
                                    <td>{{ ((new Date(item.timing)).toString()).slice(0, 16) }}</td>
                                    <td>{{ ((new Date(item.timing)).toString()).slice(16, 21) }}</td>
                                    <td><a @click="dltTheaterMovie(item.theater_movie_id)"><i class="bi bi-trash-fill"
                                                style="color: brown;"></i></a></td>
                                </tr>
                            </table>
                        </center>
                    </div>
                </div>
                <div class="col" v-else>
                    <p><i>"No Movie is running in theaters is created"</i></p>
                </div>
                <div class="col-2"></div>
            </div>
        </div><br><br>
                <center>
                <div>
                    <h6>To Add New Movie in Theater</h6>
                    <router-link to="/admin/LinkTheaterMovie"><button>+</button></router-link>
                </div>
                </center>
            </div>
</template>



<script>

import axios from 'axios';

import refreshAccessToken from '../../../utils/refreshToken'

export default {
    name: 'theaterMovieTables',
    data() {
        return {
            alltheatermovies: {},
            runningBooking: [],
            stopedBooking: [],
            running_table: false,
            stoped_table: false,
            table: false,
        }
    },
    created() {
        this.allTheaterMovies()
    },
    methods: {
        async allTheaterMovies() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const theaterMoviesResponse = await axios.get('http://127.0.0.1:8081/api/theater_movie')
                this.alltheatermovies = theaterMoviesResponse.data
                if (this.alltheatermovies.length > 0) {
                    console.log("theaterMovie data fletch")
                    this.table = true
                    for (let theatermovie of this.alltheatermovies) {
                        let time = theatermovie.timing
                        let show_time = new Date(time)
                        let time_now = new Date()
                        if (time_now < show_time) {
                            this.runningBooking.push(theatermovie)
                        }
                        else {
                            this.stopedBooking.push(theatermovie)
                        }
                    }
                    console.log(this.runningBooking)
                    if (this.runningBooking.length > 0) {
                        this.running_table = true
                    }
                    if (this.stopedBooking.length > 0) {
                        this.stoped_table = true
                    }
                }
                else {
                    console.log("No theater linked with movies")
                    this.table = false
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.allTheaterMovies()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater movie data.')
                }
            }
        },
        async dltTheaterMovie(id) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.delete(`http://127.0.0.1:8081/api/dlt/theater_movie/${id}`)
                console.log("TheaterMovie with id: " + id + " deleted")
                await this.allTheaterMovies()
            }
            catch (error) {
                console.error(error);
                alert("An error occurred while deleting Theatermovie");
            }
        }
    },
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