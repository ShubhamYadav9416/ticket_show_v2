<template>
    <div id="outer_div">
        <admin-header></admin-header>
        <div class="container-fluid text-center">
            <div class="row">
                <div class="col-2"></div>
                <div class="col" v-if="no_table">
                    <p style="margin-top: 60px; font-style: italic;">"No Table is created"</p>
                </div>
                <div class="col" v-if="show_table">
                    <table>
                        <tr>
                            <th>Theater Id</th>
                            <th>Theater Name</th>
                            <th>Theater Tag</th>
                            <th>Theater Language</th>
                            <th>Theater Duration</th>
                            <th>Theater Description</th>
                            <th>Theater Poster</th>
                            <th>Actions</th>
                        </tr>
                        <tr v-for="theater in theaters" :key="theater.theater_id">
                            <td>{{ theater.id }}</td>
                            <td>{{ theater.theater_name }}</td>
                            <td>{{ theater.theater_place }}</td>
                            <td>{{ theater.theater_location }}</td>
                            <td>{{ theater.theater_capacity }}</td>
                            <td><a href="theater.theater_image_path">view</a></td>
                            <td><a href="#"><i class="bi bi-trash-fill" style="color: brown;"></i></a>/<a href="#"><i
                                        class="bi bi-pencil-square" style="color: grey;"></i></a></td>
                        </tr>
                    </table>
                </div>
                <div class="col-2"></div>
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

                axios.defaults.headers.common['Authorization'] = 'Bearer' + access_token

                const theatersResponse = await axios.get('http://127.0.0.1:8081/api/theater')

                this.theaters = theatersResponse.data
                if (this.theaters.lenght > 0) {
                    console.log("Theater data fetched")
                    this.show_table = true
                }
                else {
                    console.log("No theater ceated")
                    this.no_table = true
                }
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    await refreshAccessToken()
                    await this.alltheaters()
                }

                else if (error.response) {
                    console.error(error)
                    alert('An error occurred while fetching the followers data.')
                }
            }
        },
    },
    components: {
        'admin-header': AdminHeader
    }
}
</script>


<style scoped>
.col {
    border: 1px solid black;
    margin: 0;
    padding: 0;
}

table {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
    border-radius: .5em;
    margin-top: 10px;
}

th {
    background-color: darkblue;
    color: white;
}

td,
th {
    padding-left: 12.5px;
    padding-right: 12.5px;
    /* border: 1px solid black; */
}

td {
    font-size: 15px;
}

tr:nth-child(even) {
    background-color: rgb(131, 202, 237);
}

tr:nth-child(odd) {
    background-color: whitesmoke;
}</style>