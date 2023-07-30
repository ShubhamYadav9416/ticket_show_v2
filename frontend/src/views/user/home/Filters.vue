<template>
    <div class="filters">
        <h3>Filters</h3>
        <div class="filter_rating">
            <dt>Filter by rating</dt>
            <dd><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i
                    class="bi bi-star-fill"></i><i class="bi bi-star"></i>
            </dd>
            <dd><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i
                    class="bi bi-star"></i><i class="bi bi-star"></i></dd>
            <dd><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star"></i><i
                    class="bi bi-star"></i><i class="bi bi-star"></i></dd>
            <dd><i class="bi bi-star-fill"></i><i class="bi bi-star"></i><i class="bi bi-star"></i><i
                    class="bi bi-star"></i><i class="bi bi-star"></i></dd>
        </div>
        <div class="filter_tags">
            <dt>Filter by Tags</dt>
            <dd>Action</dd>
            <dd>Romance</dd>
        </div>
    </div>
</template>

<script>

export default {
    name: 'userFilters',
}

</script>

<style scoped>
.filters {
    margin-top: 150px;
}

.filters h3 {
    font-size: 20px;
}

.filters dt {
    font-size: 15px;
    font-weight: 300;
}

.filters dd {
    color: rgb(232, 129, 129);
    margin-bottom: -5px;
}

.filter_tags {
    margin-top: 15px;
}

.filter_tags dd {
    color: rgb(54, 52, 52);
    font-weight: 300;
    font-size: 14px;
}

.filter_tags dd:hover {
    color: black;
    font-size: 16px;
}

.filter_rating dd:hover {
    color: red;
    font-size: 18px;
}
</style>