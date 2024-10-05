<template>
  <h6 class="fw-bold text-uppercase pb-2 mb-4">
    {{ text }}
  </h6>
</template>

<script>
export default {
  name: "SegmentTitle",
  props: {
    text: {
      type: String,
      required: true,
    },
  },
};
</script>
