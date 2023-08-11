<template>
    <div>
        <user-header></user-header>
        <div class="container-fluid text-center">
            <div class="row" style="margin-top: 60px;">
                <div class="col-2">
                    {{ theater_movies }}
                    <router-link to="/home">Return to Home Page</router-link>
                </div>
                <div class="col-10">
                    <div class="container text-center" v-show="display">
                        <div class="row" id="display_row">
                            <div class="col center-block" v-for="theater_movie in theater_movies.data"
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
import TheaterHome from '../home/TheaterHome.vue';


export default {
    name: 'search-result',
    props: ['theater_movies'],
    data() {
        return {
            // theater_movies: {},
            display:true
        }
    },
    components: {
        'user-header': UserHeaderVue,
        'theater-view': TheaterHome,
    },
}


</script>


<style scoped></style>