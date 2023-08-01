<template>
    <div>
        <user-header></user-header>
        <div class="container text-center">
            <div class="row">
                <div class="col-3">
                </div>
                <div class="col" style="padding:50px 20px">
                    User id : {{ data_recive.user_id }}<br>
                    User Mail : {{ data_recive.user_mail }}
                    <br><hr><br>
                    <div class="card mb-3" style="max-width: 540px;" v-for="ticket in data_recive.tickets" :key="ticket.id">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img :src="`data:image/jpeg;base64,${ticket.poster_url}`" class="rounded mx-auto d-block" alt="Movie Poster" style="max-height: 300px; max-width: 150px; margin-top:7px;">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">{{ ticket.movie_name }}</h5>
                                    <p style="color:rgb(103, 101, 101); margin-top:-10px; font-size:13px;">{{ ticket.movie_tag }} | {{ ticket.movie_language }} | {{ ticket.movie_duration }}</p>
                                    <i class="bi bi-pin-map-fill" style="color:green;"></i>{{ ticket.theater_name }}, {{ ticket.theater_place }}, {{ ticket.theater_location }}<br>
                                    <p><i class="bi bi-clock"></i> {{ new Date(ticket.show_time).getDate() }}/{{ new Date(ticket.show_time).getMonth() }}/{{ new Date(ticket.show_time).getFullYear() }}  {{ new Date(ticket.show_time).getHours() }}:{{ new Date(ticket.show_time).getMinutes() }} </p>

                                    <p align="left" style="margin-top:10px; margin-left:-15px;">No. of Tickets : &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {{ ticket.no_of_tickets }}</p>
                                    <p align="left" style="margin:-15px;">Total Paid : &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; Rs. {{ ticket.price }}</p>
                                    <p style="margin-top: 20px; font-size:10px">Booking Id: {{ ticket.booking_id }} <i class="bi bi-clock"></i> {{ ticket.booking_time }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-3">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

import refreshAccessToken from '../../../utils/refreshToken'
import UserHeader from '@/components/UserHeader.vue';

export default {
    name: 'UserBooking',
    data() {
        return{
            data_recive:{}
        }
    },
    created() {
        this.userBookings()
    },
    methods: {
        async userBookings() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersMoviebookingResponse = await axios.get(`http://127.0.0.1:8081/api/user/bookings`)
                this.data_recive = theatersMoviebookingResponse.data 
                console.log(this.data_recive.tickets[0])
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.userBookings()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the movie data.')
                }
            }
        }
    },
    components: {
        'user-header': UserHeader,
    },
}

</script>


<style scoped>
.col {
    border: 1px solid rgb(230, 227, 227);
}
</style>