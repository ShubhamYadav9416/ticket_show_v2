<template>
    <div>
        <user-header></user-header>
        <div class="container text-center">
            <div class="row" id="outer">
                <div class="col-2">

                </div>
                <div class="col">
                    <div class="container text-center">
                        <div class="row" style="padding: 10px;" id="inner">
                            <div class="col-7" align="left">

                                <h5>Antman and The Wasp Quantumania</h5>
                                <p style="font-size: small; color: rgb(71, 69, 69);">Action | English | 2 hr 5 min</p>
                                <p style="font-weight: 300;">This is a Marvel Universe moie, In the the mistrey
                                    of muliverse is solved.</p>
                                <p class="location"><i class="bi bi-geo-alt-fill" style="color:green"></i>PVR ,connaught
                                    palace,
                                    New delhi, 110012
                                </p>
                                <span style="font-size: small;">Per Ticket Rs<i style="font-size: medium;">{{ cost_per_ticket }}</i></span>
                                <div class="d-flex align-items-end">
                                    <button class="minus_button" @click="minus()">-</button>
                                    <input style="width: 50px; height: 40px;" v-model="no_of_tickets">
                                    <button class="plus_button" @click="plus()">+</button>
                                    <p v-show="price">Your Total Rs {{ price }} only.</p>
                                    <button type="button" class="btn btn-success" style="margin-left: 20px;"
                                        v-show="no_of_tickets > 0">Book</button>
                                </div>
                                <span style="font-size: small;">Hurry up!! only <i style="font-size: medium;">56</i>
                                    left.</span>
                            </div>
                            <div class="col-1"></div>
                            <div class="col-4">
                                <img src="../../../assets/ant-man-and-the-wasp-quantumania.avif"
                                    class="rounded mx-auto d-block" alt="..." style="max-height: 350px; max-width: 175px;">
                            </div>
                            
                        </div>
                    </div>
                </div>
                <div class="col-2 d-flex align-items-start">
                    <router-link to="/home">
                    <button type="button" class="btn-close" aria-label="Close" style="margin-left: -20px;margin-top: -10px;"></button>
                </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserHeader from '@/components/UserHeader.vue';

export default {
    name: 'MovieBooking',
    data() {
        return {
            no_of_tickets: 0,
            cost_per_ticket: 80,
            price: "",
        }
    },
    methods: {
        minus() {
            if (this.no_of_tickets === 0) {
                this.no_of_tickets = 0
                this.price = ""
            }
            else {
                this.no_of_tickets = this.no_of_tickets - 1
                this.price = this.no_of_tickets * this.cost_per_ticket
            }
        },
        plus() {
            if (!this.no_of_tickets) {
                this.no_of_tickets = 1
                this.price = this.no_of_tickets * this.cost_per_ticket
            }
            else {
                this.no_of_tickets = this.no_of_tickets + 1
                this.price = this.no_of_tickets * this.cost_per_ticket
            }
        }
    },
    components: {
    'user-header': UserHeader,
},

}


</script>


<style scoped>
#outer {
    margin-top: 90px;
}

#inner {
    border: 1px solid rgb(86, 85, 87);
    border-radius: 5px;
}



.minus_button {
    width: 50px;
    height: 40px;
    border-radius: 10px 0px 0 10px;
    font-size: 20px;
    font-weight: bolder;
    background-color: brown;
}

.plus_button {
    width: 50px;
    height: 40px;
    padding: 0;
    border-radius: 0px 10px 10px 0px;
    font-size: 20px;
    font-weight: bolder;
    background-color: darkgreen;

}
</style>