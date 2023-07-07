<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container text-center">
            <div class="row">
                <div class="col-4">

                </div>
                <div class="col">
                    <br><br>
                    <p>To add new Movie<br> Fill this form</p>
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_name" required placeholder="Movie Name">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_tag" required placeholder="Movie Tag">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_language" required
                                placeholder="Movie Language">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_duration" required
                                placeholder="Movie Duration">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_description" required
                                placeholder="Movie Description">
                        </div>
                        <div class="input-group mb-3">
                            <input type="file" class="form-control" id="inputGroupFile01">
                        </div>
                        <button type="submit" class="btn btn-primary">Add Movie</button>
                    </form>
                </div>
                <div class="col-4">

                </div>
            </div>
        </div>
    </div>
</template>



<script>

import AdminHeader from '../../../components/AdminHeader.vue'


export default {
    components: {
        'admin-header': AdminHeader
    }
}
</script>


<style scoped></style>