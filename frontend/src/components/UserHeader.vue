<template>
    <div class="container-fluid text-center" id="header">
        <div class="row">
            <div class="col-2">
                <div class="container-fluid text-center">
                    <div class="row">
                        <div class="col" style="background-color: rgb(55, 31, 149);"></div>
                        <div class="col" id="logo-div">
                            <router-link to="/home"><img src="../assets/logo.png"></router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-2" style="background-color: rgba(77,70,163,255);"></div>
            <div class="col-3" style="background-color: rgba(77,70,163,255);">
                <router-link to="/search" style="text-decoration: none;"><input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" style="height: 24px; margin: 5px; border: 0;"></router-link>
            </div>
            <div class="col-1" style="background-color: rgba(77,70,163,255);"></div>
            <div class="col-4" style="background-color: rgba(77,70,163,255);">
                <router-link style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    to="/bookings"><span id="links">Bookings</span></router-link>
                <i style="text-decoration: none; color: rgb(228, 222, 222); font-weight: 300; margin-right: 10px;"
                    @click="logoutUser()"><span id="link_logout">LogOut</span></i>
                <span class="dot">S</span>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'adminHeader',

    methods: {
        async logoutUser() {
            try {
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user_mail')

                alert('User Successfully logged out !!')
                this.$router.push('/login')
            }
            catch (error) {
                console.log(error)
            }
        },
    }
}

</script>

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
.col{
    padding: 0;
    margin: 0;
}
.col-4 {
    margin: 0;
    padding: 5px 0 0 0;
}

.dot {
    height: 25px;
    width: 25px;
    background-color: #505a3a;
    border-radius: 50%;
    display: inline-block;
    color: white;
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
    color: rgb(250, 250, 252);
    font-weight: bolder;
}

#link_logout:hover {
    color: red;
    font-weight: bolder;
}
</style>