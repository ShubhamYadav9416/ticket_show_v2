<template>
    <div class="outer_modal">
        <div class="modal">
            <div class="modal-content">
                <p>{{ message }}</p>
                <div class="btn-group" role="group" aria-label="Basic mixed styles example">
                    <button type="button" class="btn btn-primary" @click="cancel" style="margin-right: 20%;">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="confirm">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        message: String,
        onConfirm: Function,
        onCancel: Function
    },
    methods: {
        confirm() {
            this.onConfirm();
        },
        cancel() {
            this.onCancel();
        }
    }
};
</script>
  
<style scoped>
.modal {
    position: fixed;
    top: 0;
    left: 40%;
    width: 20%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}
</style>
  