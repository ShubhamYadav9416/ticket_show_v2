<template>
<div id="outer_div">
        <admin-header></admin-header>
        <div class="container text-center">
          <div class="row">
                <div class="col-4">

                </div>
                <div class="col">
                    <br><br>
                    <p>To edit Movie<br> Fill this form</p>
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_name" required
                      placeholder="Movie Name" >
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_tag" required
                                placeholder="Movie Tag">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie_language" required
                                placeholder="Movie Language" >
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
                        <button type="button" class="btn btn-primary" @click="editMovie()">Edit Movie</button>
                    </form>
                </div>
                <div class="col-4">

                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import refreshAccessToken from '../../../utils/refreshToken';

import AdminHeader from '../../../components/AdminHeader'


export default {
    name: 'EditMovie',
    data(){
        return {
            movie_id : this.$route.params.id,
            movie: {},
            movie_name: '',
            movie_tag: '',
            movie_language: '',
            movie_duration: '',
            movie_description: '',
        }
    },
    created(){
        this.fetchMovie()
    },
    methods: {
        async fetchMovie(){
            try{
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                const movieResponse = await axios.get(`http://127.0.0.1:8081/api/movie/${this.movie_id}`)
                this.movie = movieResponse.data
                this.movie_name = this.movie.movie_name
                this.movie_tag = this.movie.movie_tag
                this.movie_language = this.movie.movie_language
                this.movie_duration = this.movie.movie_duration
                this.movie_description = this.movie.movie_description
                console.log(this.movie.movie_name)
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.fetchMovie()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the movie data.')
                }
            }
        },
        async editMovie() {
            if (!this.movie_name || !this.movie_tag || !this.movie_language || !this.movie_duration || !this.movie_description) {
                alert("All fields are required !!");
                return;
            }
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.put(`http://127.0.0.1:8081/api/movie/${this.movie_id}`, {
                    movie_name: this.movie_name,
                    movie_tag: this.movie_tag,
                    movie_language: this.movie_language,
                    movie_duration: this.movie_duration,
                    movie_description: this.movie_description,
                })
                this.$router.push("/admin/movie");
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.editMovie();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    alert('An error occurred while editing movie.')
                }
            }

        }
    },
    components: {
        'admin-header': AdminHeader
    }
}

</script>