<template>
    <div class="container-fluid text-center" id="header">
        <div class="row">
            <div class="col-2">
                <div class="container-fluid text-center">
                    <div class="row">
                        <div class="col" style="background-color: rgb(55, 31, 149);"></div>
                        <div class="col" id="logo-div">
                            <router-link to="/admin/dashboard"><img src="../assets/logo.png"></router-link>
                        </div>
                        <div class="col" style="background-color: rgba(77,70,163,255); color: red;"><span
                                id="Admin_blink">Admin</span></div>
                    </div>
                </div>
            </div>
            <div class="col-2" style="background-color: rgba(77,70,163,255);"></div>
            <div class="col-2" style="background-color: rgba(77,70,163,255);"></div>
            <div class="col-2" style="background-color: rgba(77,70,163,255);"></div>
            <div class="col-4" style="background-color: rgba(77,70,163,255);">
                <router-link style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    to="/admin/dashboard"><span id="links">Dashboard</span></router-link>
                <router-link style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    to="/admin/movie"><span id="links">Movies</span></router-link>
                <router-link style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    to="/admin/theater"><span id="links">Theaters</span></router-link>
                <router-link style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    to="#"><span id="link_logout">LogOut</span></router-link>
            </div>
        </div>
    </div>
</template>


<style scoped>
#outer_div {
    border: 1px solid black;
}

.col-2 {
    margin: 0;
    padding: 0;
}

.col-2 .col {
    margin: 0;
    padding: 0;
}

.col-4 {
    margin: 0;
    padding: 5px 0 0 0;
}

img {
    margin: 0;
    height: 35px;
    width: 120.5px;
}

#Admin_blink {
    animation: animate 3s linear infinite;
}

@keyframes animate {
    0% {
        opacity: 0.3;
    }

    50% {
        opacity: 0.7;
    }

    100% {
        opacity: 1;
    }
}

#logo-div {
    margin: 0;
    padding: 0;
}

#links:hover {
    color: rgb(3, 5, 110);
    font-weight: bolder;
}

#link_logout:hover {
    color: red;
    font-weight: bolder;
}
</style>