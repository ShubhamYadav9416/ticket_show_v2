<template>
    <div>
        <div class="container text-center">
            <div class="row">
                <div class="col-3"></div>
                <div class="col-6">
                    <div class="logo-div">
                        <img src="../../assets/logo.png">
                    </div>
                    <div class="inner-box">
                    <div class="buttons-div">
                        <div class="container text-center">
                            <div class="row">
                                <div class="col-5">
                                    <router-link to="/login"><button class="current_btn">Login</button></router-link>
                                </div>
                                <div class="col-2">
                                </div>
                                <div class="col-5">
                                    <router-link to="/register"><button class="other_btn">Register</button></router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <form>
                            <div class="mb-3">
                                <input type="email" class="form-control" id="exampleInputEmail1" v-model="user_mail"
                                    aria-describedby="emailHelp" placeholder="Email Address">
                            </div>
                            <div class="mb-3">
                                <input type="password" class="form-control" id="exampleInputPassword1" v-model="password"
                                    placeholder="Password">
                            </div>
                            <input type="submit" class="form-control" id="submit" @click.prevent="loginUser()">
                        </form>
                        </div>
                    </div>
                </div>
                <div class="col-3"></div>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';

export default{
    name: 'LoginView',
    data(){
        return{
            user_mail: "",
            password: "",
        }
    },
    methods: {
        loginUser(){
            if (!this.user_mail || !this.password){
                alert("Please enter both the user mail and password");
                return;
            }
            axios.post("http://127.0.0.1:8081/api/login", {
                user_mail : this.user_mail,
                password : this.password,
            }) .then((response) => {
                if (response.data.status === "success"){
                    if(response.data.admin === false){alert("Normal user login")
                    const access_token = response.data.access_token;
                    const refresh_token = response.data.refresh_token;
                    const user_mail = response.data.user_mail;


                    localStorage.setItem("access_token", access_token);
                    localStorage.setItem("refresh_token", refresh_token);
                    localStorage.setItem("user_mail", user_mail);

                    console.log(access_token);
                    console.log(response.data.admin);
                    this.$router.push("/home");
                    return;
                }
                }
                if (response.data.status === "success" ){
                    if (response.data.admin == true){
                    const access_token = response.data.access_token;
                    const refresh_token = response.data.refresh_token;
                    const user_mail = response.data.user_mail;


                    localStorage.setItem("access_token", access_token);
                    localStorage.setItem("refresh_token", refresh_token);
                    localStorage.setItem("user_mail", user_mail);

                    console.log(access_token);
                    console.log(response.data.admin);

                    this.$router.push("/admin/dashboard"); 
                    }
                }
                if (response.data.status === 'failed'){
                    alert(response.data.message)
                }
            })
        }
    }
}

</script>

<style scoped>
.logo-div{
    background-color: rgb(74, 64, 161);
}
img {
    height: 30%;
    width: 30%;
}
.inner-box{
    padding: 0px 20px 25px 20px;
}
.buttons-div {
    margin-top: 20px;
    padding: 0 20px 0 20px;
}


.current_btn {
    font-weight: 300;
    font: "Courier New";
    /* font-size: 10px; */
    color: darkblue;
    background-color: rgb(214, 235, 250);
    border-radius: .2rem;
    border-width: 0.5px;
    border-color: rgb(62, 188, 230);
    width: 100%;
    padding-top: 7px;
    padding-bottom: 7px;
}

.other_btn {
    font-weight: 300;
    font: "Courier New";
    /* font-size: 10px; */
    color: rgb(42, 56, 43);
    background-color: rgb(233, 234, 234);
    border-width: 0px;
    border-radius: .2rem;
    border-color: rgb(62, 188, 230);
    width: 100%;
    padding-top: 7px;
    padding-bottom: 7px;
    opacity: 0.8;
}

form {
    margin-top: 20px;
    padding: 0 30px 0 30px;
}

#submit {
    background-color: blue;
    color: white;
    font-weight: bolder;
}

.col-6 {
    padding: 0;
    margin-top: 200px;
    border: 1px solid black;
}</style>