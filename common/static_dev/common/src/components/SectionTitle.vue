<template>
  <div
    class="section-title"
    :class="{ 'border-bottom pb-3': borderBottom }">
    <h6 class="mb-1">
      {{ title }}
    </h6>
    <div>{{ description }}</div>
  </div>
</template>

<script>
export default {
  name: "SectionTitle",
  props: {
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    borderBottom: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>
