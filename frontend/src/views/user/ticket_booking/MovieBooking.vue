<template>
    <div>
        <user-header></user-header>
        <div class="container text-center">
            <div class="row" id="outer">
                <div class="col-2">

                </div>
                <div class="col">
                    <div class="container text-center">
                        <div class="row" style="padding: 10px;" id="inner">
                            <div class="col-7" align="left">
                                <h5>{{ movie_data.movie_name }}</h5>
                                <p style="font-size: small; color: rgb(71, 69, 69);">{{ movie_data.movie_tag }} | {{
                                    movie_data.movie_language }} | {{ movie_data.movie_duration }}</p>
                                <p style="font-weight: 300;">{{ movie_data.movie_description }}</p>
                                <p class="location"><i class="bi bi-geo-alt-fill" style="color:green"></i>{{
                                    movie_data.theater_place }} , {{ movie_data.theater_location }}
                                </p>
                                <span style="font-size: small;">Per Ticket Rs<i style="font-size: medium;">{{
                                    movie_data.current_price }}<i class="bi bi-arrow-down-right" style="color:green;" v-show="movie_data.current_price < movie_data.start_price"></i><i class="bi bi-arrow-up-left" style="color:red;" v-show="movie_data.current_price > movie_data.start_price"></i> </i></span>
                                <div class="d-flex align-items-end" v-show="!booking_close">
                                    <button class="minus_button" @click="minus()">-</button>
                                    <input style="width: 50px; height: 40px;" v-model="no_of_tickets">
                                    <button class="plus_button" @click="plus()">+</button>
                                    <p v-show="price">Pay Rs {{ price }}.00</p>
                                    <button type="button" class="btn btn-success" style="margin-left: 20px;"
                                        v-show="no_of_tickets > 0"  @click="bookTicket()">Book</button>
                                </div>
                                <span style="font-size: small;">Hurry up!! only <i style="font-size: medium;">{{
                                    movie_data.seat_left }}</i>
                                    left.</span>
                            </div>
                            <div class="col-1"></div>
                            <div class="col-4">
                                <img :src="`data:image/jpeg;base64,${movie_data.poster_url}`" class="rounded mx-auto d-block" alt="..." style="max-height: 350px; max-width: 175px;">
                            </div>

                        </div>
                    </div>
                </div>
                <div class="col-2 d-flex align-items-start">
                    <router-link to="/home">
                        <button type="button" class="btn-close" aria-label="Close"
                            style="margin-left: -20px;margin-top: -10px;"></button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserHeader from '@/components/UserHeader.vue';
import axios from 'axios';

import refreshAccessToken from '../../../utils/refreshToken'



export default {
    name: 'MovieBooking',
    data() {
        return {
            theater_movie_id: this.$route.params.id,
            no_of_tickets: "",
            movie_data: [],
            price: "",
            cost_per_ticket: "",
            booking_close:false,
        }
    },
    created() {
        this.movieDataBooking()
    },
    methods: {
        minus() {
            if (this.no_of_tickets === 0) {
                this.no_of_tickets = 0
                this.price = ""
            }
            else if (this.no_of_tickets < 0) {
                this.booking_close = true
            }
            else {
                this.no_of_tickets = this.no_of_tickets - 1
                this.price = this.no_of_tickets * this.cost_per_ticket
            }
        },
        plus() {
            if (!this.no_of_tickets) {
                this.no_of_tickets = 1
                this.price = this.no_of_tickets * this.cost_per_ticket
            }
            else {
                let max_ticket = this.movie_data.seat_left
                if (max_ticket == 0){
                    this.booking_close = true
                }
                else if (max_ticket > 9){
                    if (this.no_of_tickets > 8){
                    this.no_of_tickets = 9
                    this.price = this.no_of_tickets * this.cost_per_ticket
                    }
                    else{
                    this.no_of_tickets = this.no_of_tickets + 1
                    this.price = this.no_of_tickets * this.cost_per_ticket
                    }
                }
                else{
                    if (this.no_of_tickets > max_ticket-1){
                    this.no_of_tickets = max_ticket
                    this.price = this.no_of_tickets * this.cost_per_ticket
                    }
                    else{
                    this.no_of_tickets = this.no_of_tickets + 1
                    this.price = this.no_of_tickets * this.cost_per_ticket
                    }
                }
                // if (this.movie_data.seat_left > 9){
                //     this.no_of_tickets = this.no_of_tickets + 1
                //     this.price = this.no_of_tickets * this.cost_per_ticket
                // }
                // else if (this.movie_data.seat_left < 10){
                //     this.no_of_tickets = this.movie_data.seat_left
                //     this.price = this.no_of_tickets * this.cost_per_ticket
                // }
            }
        },
        async movieDataBooking() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersMoviebookingResponse = await axios.get(`http://127.0.0.1:8081/api/theater_movie/booking/${this.theater_movie_id}`)
                this.movie_data = theatersMoviebookingResponse.data[0]
                this.cost_per_ticket = this.movie_data.current_price
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.movieDataBooking()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the movie data.')
                }
            }
        },
        async bookTicket(){
            if (!this.no_of_tickets) {
                alert("Add Number of Ticekt !!");
                return;
            }
            try {

                let formData = new FormData()

                formData.append('data',JSON.stringify({
                    no_of_tickets : this.no_of_tickets,
                    total_paid : this.price
                }))
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                console.log(typeof this.no_of_tickets)
                await axios.post(`http://127.0.0.1:8081//api/book_ticket/${this.theater_movie_id}`, formData)
                this.$router.push("/bookings");
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.bookTicket();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    alert('An error occurred while ticket booking.')
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
#outer {
    margin-top: 90px;
}

#inner {
    border: 1px solid rgb(86, 85, 87);
    border-radius: 5px;
}



.minus_button {
    width: 50px;
    height: 40px;
    border-radius: 10px 0px 0 10px;
    font-size: 20px;
    font-weight: bolder;
    background-color: brown;
}

.plus_button {
    width: 50px;
    height: 40px;
    padding: 0;
    border-radius: 0px 10px 10px 0px;
    font-size: 20px;
    font-weight: bolder;
    background-color: darkgreen;

}</style>