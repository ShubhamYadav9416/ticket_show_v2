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
                            <input type="text" class="form-control" v-model="movie.movie_name" required 
                                placeholder="Movie Name">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie.movie_tag" required 
                                placeholder="Movie Tag">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie.movie_language" required
                                placeholder="Movie Language">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie.movie_duration" required
                                placeholder="Movie Duration">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="movie.movie_description" required
                                placeholder="Movie Description">
                        </div>
                        <div class="input-group mb-3">
                            <input type="file" class="form-control" id="inputGroupFile01" @change="onFileSelected">
                        </div>
                        <button type="button" class="btn btn-primary" @click="addMovie()">Add Movie</button>
                    </form>
                </div>
                <div class="col-4">

                </div>
            </div>
        </div>
    </div>
</template>



<script>
import axios from 'axios';
import AdminHeader from '../../../components/AdminHeader.vue'
import refreshAccessToken from '../../../utils/refreshToken';


export default {
    name: "AddTheater",
    data() {
        return {
            movie: {
                movie_name: '',
                movie_tag: '',
                movie_language: '',
                movie_duration: '',
                movie_description: '',
            },
            movie_poster: null,
        }
    },
    components: {
        'admin-header': AdminHeader
    },
    methods: {
        async addMovie() {
            if (!this.movie.movie_name || !this.movie.movie_tag || !this.movie.movie_language || !this.movie.movie_duration || !this.movie.movie_description) {
                alert("All fields are required !!");
                return;
            }

            let formData = new FormData()

            formData.append('data',JSON.stringify(this.movie))

            if (this.movie_poster) {
                formData.append('movie_poster', this.movie_poster)
            }
            console.log(this.movie_poster)
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post("http://127.0.0.1:8081/api/movie", formData)
                console.log('hello')
                console.log(formData.values().next())
                this.$router.push("/admin/movie");
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.addMovie();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    console.log(error)
                    alert('An error occurred while creating movie')
                }

                else if (error.response && error.response.status === 409) {
                    alert(error.response.data.message)
                }
            }

        },
        onFileSelected(event) {
            this.movie_poster = event.target.files[0]
        }
    }
}
</script>


<style scoped></style>