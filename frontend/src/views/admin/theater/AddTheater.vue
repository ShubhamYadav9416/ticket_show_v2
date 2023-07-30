<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container text-center">
            <div class="row">
                <div class="col-4">

                </div>
                <div class="col">
                    <br><br>
                    <p>To add new Theater<br> Fill this form</p>
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="theater_name" required
                                placeholder="Theater Name">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="theater_place" required
                                placeholder="Theater place">
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" v-model="theater_location" required
                                placeholder="Theater Location">
                        </div>
                        <div class="mb-3">
                            <input type="number" class="form-control" v-model="theater_capacity" required
                                placeholder="Theater Capacity">
                        </div>
                        <button type="button" class="btn btn-primary" @click="addTheater()">Add Theater</button>
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
            theater_name: '',
            theater_place: '',
            theater_location: '',
            theater_capacity: '',
        }
    },
    components: {
        'admin-header': AdminHeader
    },
    methods: {
        async addTheater() {
            if (!this.theater_name || !this.theater_place || !this.theater_location || !this.theater_capacity) {
                alert("All fields are required !!");
                return;
            }
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token

                await axios.post("http://127.0.0.1:8081/api/theater", {
                    theater_name: this.theater_name,
                    theater_place: this.theater_place,
                    theater_location: this.theater_location,
                    theater_capacity: this.theater_capacity,
                })
                this.$router.push("/admin/theater");
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken();
                    await this.addTheater();
                }

                else if (error.response && error.response.status === 400 || error.response.status === 422) {
                    this.errors = error.response.data.errors;
                    alert('An error occurred while creating theater.')
                }
            }

        }
    }
}
</script>


<style scoped></style>