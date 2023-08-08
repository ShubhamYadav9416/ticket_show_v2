<template>
  <div class="container text-center">
  <div class="row">
    <div class="col-1"></div>
    <div class="col-6">
      <span align="left"><p>CINEPASS <i style="font-size: small; color: rgb(106, 103, 103);">Ticket Show v2</i></p></span>
      <span align="left"><p>This is a Movie Ticket Booking Website which is made as Course Project of Modern Application Development 2 in 
                            BS in Data Science and Application of Indian Institue of Technology, Madras. </p></span>
      <span align="left"><p>VUE.js used for UI. Flask  restful API used for data Tranfer and for interaction with server.
        SQLite is used for Data Storage. In backend Flask Caching is used for effectiveness, with redis. Celery is used with
        redis and celery beats asynchronously execute work outside the HTTP request-response cycle. 
      </p></span>
      <span align="left"><p>Two type of interfaces, Admin interface (fixed mail: <b>admin@gmail.com</b> and password: <b>1234</b>)
      and User interface.</p></span>
      <span align="left"><p>To Know more about app read Documentaion</p></span>
      <router-link to="/login"><button type="button" class="btn btn-outline-primary">Lets Go !!</button></router-link>

    </div>
    <div class="col-5"></div>
  </div>
</div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>

<style scoped>
.col-6{
  /* border: 1px solid rgb(210, 199, 199); */
  margin-top: 100px;
  padding-bottom: 20px;
}
</style>
