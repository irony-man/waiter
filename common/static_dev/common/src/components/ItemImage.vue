<template>
  <img
    :src="item.image || `https://placehold.co/96x96/FEE2E2/dc3545?text=${item.name.substring(0, 2).toUpperCase()}`"
    :alt="item.name"
    class="img-fluid rounded-lg"
    style="width: 96px; height: 96px; object-fit: cover;"
    onerror="this.onerror=null;this.src='https://placehold.co/96x96/FEE2E2/dc3545?text=N/A';">
</template>

<script>
export default {
  name: 'ItemImage',
  props: {
    item: {
      type: Object,
      required: true
    }
  }
};
</script>
