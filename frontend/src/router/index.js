import Vue from "vue";
import VueRouter from "vue-router";


import RegisterView from "../views/auth/RegisterView.vue";
import LoginView from "../views/auth/LoginView.vue";
import DashboardView from "../views/admin/DashboardView.vue";
import AddMovie from "../views/admin/movies/AddMovie.vue";
import MovieView from "../views/admin/movies/MovieView.vue";
import AddTheater from "../views/admin/theater/AddTheater.vue";
import TheaterView from "../views/admin/theater/TheaterView.vue"


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
        path : "/admin/theater",
        name : "Admin-Theater",
        component : TheaterView,
    },
    {
        path: "/admin/add_theater",
        name: "Add-Theater",
        component : AddTheater,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;