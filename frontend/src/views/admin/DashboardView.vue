<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <theatermovie-tables></theatermovie-tables>
    </div>
</template>



<script>

import AdminHeader from '../../components/AdminHeader'
import theaterMovieTables from '../admin/theater_movie/TheaterMovieView.vue'

export default{
    components:{
        'admin-header' : AdminHeader,
        'theatermovie-tables' : theaterMovieTables
    }
}
</script>


<style scoped>

</style>