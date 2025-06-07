<template>
  <div>
    <span
      v-if="menuType === 'VEG'"
      class="text-success me-2"
      title="Vegetarian">
      <i class="fas fa-leaf"/>
    </span>
    <span
      v-else
      class="text-danger me-2"
      title="Non-Vegetarian">
      <i class="fas fa-drumstick-bite"/>
    </span>
  </div>
</template>

<script>
export default {
  name: 'ItemIcon',
  props: {
    menuType: {
      type: String,
      required: true
    }
  }
};
</script>
