<template>
  <div class="card bg-primary-subtle text-center h-100">
    <div class="icon-img-container">
      <img
        v-if="category.image"
        :src="category.image"
        :alt="category.name">
      <img
        v-else
        src="@/assets/images/plate.png"
        :alt="category.name">
    </div>
    <div class="card-body">
      <div class="card-text fw-normal">
        {{ category.name }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryCard',
  props: {
    category: {
      type: Object,
      required: true
    }
  }
};
</script>
