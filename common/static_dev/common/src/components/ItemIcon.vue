<template>
  <div class="is-20 me-2 mb-2">
    <img
      v-if="menuType === 'VEG'"
      class="is-20"
      src="@/assets/images/veg.png"
      alt="Veg">
    <img
      v-else
      class="is-20"
      src="@/assets/images/non-veg.png"
      alt="Non Veg">
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
