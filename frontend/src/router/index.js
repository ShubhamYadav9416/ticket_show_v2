import Vue from "vue";
import VueRouter from "vue-router";


import RegisterView from "../views/auth/RegisterView.vue";
import LoginView from "../views/auth/LoginView.vue";
import ForgetPassView from "../views/auth/ForgetPassView.vue";

import DashboardView from "../views/admin/DashboardView.vue";
import AddMovie from "../views/admin/movies/AddMovie.vue";
import MovieView from "../views/admin/movies/MovieView.vue";
import EditMovie from "../views/admin/movies/EditMovie.vue"
import AddTheater from "../views/admin/theater/AddTheater.vue";
import TheaterView from "../views/admin/theater/TheaterView.vue";
import EditTheater from "../views/admin/theater/EditTheater.vue"
import LinkTheaterMovie from "../views/admin/theater_movie/LinkTheaterMovie.vue"
import Home from "../views/user/home/Home.vue"
import MovieBooking from "../views/user/ticket_booking/MovieBooking.vue"
import UserBooking from "../views/user/booked/UserBookig.vue"

Vue.use(VueRouter);

const routes = [
    {
        path: "/register",
        name: "Registration-Page",
        component : RegisterView,
    },
    {
        path: "/login",
        name: "LoginView",
        component : LoginView,
    },
    {
        path: "/forget_password",
        name: "ForgetPassView",
        component: ForgetPassView,
    },
    {
        path : "/admin/dashboard",
        name : "Admin-Dashboard",
        component : DashboardView,
    },
    {
        path: "/admin/movie",
        name: "Admin-Movie",
        component : MovieView,
    },
    {
        path: "/admin/add_movie",
        name: "Add-Movie",
        component : AddMovie,
    },
    {
        path: "/admin/movie/edit/:id",
        name: "Edit-Movie",
        component: EditMovie,
    },
    {
        path : "/admin/theater",
        name : "Admin-Theater",
        component : TheaterView,
    },
    {
        path: "/admin/add_theater",
        name: "AddTheater",
        component : AddTheater,
    },
    {
        path: "/admin/theater/edit/:id",
        name: "Edit-Theater",
        component: EditTheater,
    },
    {
        path: "/admin/LinkTheaterMovie",
        name: "Link-TheaterMovie",
        component: LinkTheaterMovie,
    },
    {
        path: "/home",
        name: "User-Home",
        component: Home,
    },
    {
        path: "/bookings",
        name: "user-bookings",
        component: UserBooking,
    },
    {
        path: "/movie/booking/:id",
        name: "Movie-Booking",
        component: MovieBooking,
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;