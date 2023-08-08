<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container-fluid text-center" style="margin-bottom: 40px;">
            <div class="row">
                <div class="col"></div>
                <div class="col" v-show="no_table">
                    <p style="margin-top: 60px; font-style: italic;">"No Theater is created"</p><br><br>
                </div>
                <div class="col" v-if="show_table">
                    <h3 style="margin-top: 20px;">All Theaters</h3>
                    <table>
                        <tr>
                            <th>Theater Id</th>
                            <th>Theater Name</th>
                            <th>Theater Place</th>
                            <th>Theater Loaction</th>
                            <th>Theater Capacity</th>
                            <th>Actions</th>
                            <th>Export CSV</th>

                        </tr>
                        <tr v-for="theater in theaters" :key="theater.theater_id">
                            <td>{{ theater.theater_id }}</td>
                            <td>{{ theater.theater_name }}</td>
                            <td>{{ theater.theater_place }}</td>
                            <td>{{ theater.theater_location }}</td>
                            <td>{{ theater.theater_capacity }}</td>
                            <td><a id="dlt" @click="dltTheater(theater.theater_id)"><i class="bi bi-trash-fill" style="color: brown;"></i></a>/
                                <router-link  :to="`/admin/theater/edit/${theater.theater_id}`"><i class="bi bi-pencil-square" style="color: grey;"></i></router-link></td>
                            <td> <button type="button" class="btn btn-primary" @click="triggerCSVExport(theater.theater_id)"><i class="bi bi-cloud-arrow-down"></i></button> </td>

                        </tr>
                    </table>
                </div>
                <div class="col"></div>
            </div>
        </div>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-3"></div>
                <div class="col">
                    <div class="container text-center">
                        <div class="row">
                            <div class="col">
                                <h6>To Add New Theater</h6>
                                <router-link to="/admin/add_theater"><button class="add_button"><center>+</center></button></router-link>
                            </div>
                            <div class="col"></div>
                            <div class="col">
                                <h6>To Add New Movie in Theater</h6>
                                <router-link to="/admin/LinkTheaterMovie"><button class="add_button">+</button></router-link>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-3"> </div>
            </div>
        </div>
    </div>
</template>



<script>

import axios from 'axios';
import AdminHeader from '../../../components/AdminHeader'

import refreshAccessToken from '../../../utils/refreshToken'

export default {
    data() {
        return {
            theaters: {},
            show_table: false,
            no_table: false,
        }

    },
    created() {
        this.allTheaters()
    },
    methods: {
        async allTheaters() {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                const theatersResponse = await axios.get('http://127.0.0.1:8081/api/theater')

                this.theaters = theatersResponse.data
                if (this.theaters.length > 0) {
                    console.log("Theater data fetched")
                    this.no_table=false
                    this.show_table = true
                }
                else {
                    console.log("No theater ceated")
                    this.no_table = true
                    this.show_table = false
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.alltheaters()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the theater data.')
                }
            }
        },
        async dltTheater(id){
            try{
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
            
                await axios.delete(`http://127.0.0.1:8081/api/theater/${id}`)
                console.log("theater with id: " + id + " deleted")
                await this.allTheaters()
            }
            catch (error){
                console.error(error);
                alert("Theater has Movie running.");
            }

        },
        async triggerCSVExport(id) {
            try {
                let access_token = localStorage.getItem('access_token')

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token
                await axios.get(`http://127.0.0.1:8081/api/export_csv/${id}`)
                alert("CSV Fill Sent on Your Email")
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.triggerCSVExport(id)
                }
                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while exporting the theater data.')
                }
            }
        }
    },
    components: {
        'admin-header': AdminHeader
    }
}
</script>


<style scoped>
.col {
    /* border: 1px solid black; */
    margin: 0;
    padding: 0;
}

.add_button{
    background-color: rgb(165, 165, 231);
    border: 0;
    color: white;
    width: 50px;
    height: 50px;
    font-size: 25px;
    text-align: center;
    border-radius: 2rem;
}
.add_button:hover{
    background-color: rgb(126, 126, 230);
}
table {
    /* border: 1px solid black; */
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
    font-size: 15px;
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