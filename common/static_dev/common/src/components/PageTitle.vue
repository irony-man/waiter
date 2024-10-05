<template>
  <div class="d-flex gap-3 flex-column flex-md-row align-items-md-center mb-4 pb-3">
    <div class="d-flex flex-grow-1 align-items-center">
      <div
        v-if="icon"
        class="text-primary me-4">
        <i :class="icon"/>
      </div>
      <div>
        <div
          class="letter-spacing-1 text-muted small mb-1"
          v-html="secondary"/>
        <h4
          class="text-uppercase fw-bold mb-0"
          v-html="primary"/>
      </div>
    </div>
    <slot name="right"/>
  </div>
</template>

<script>
export default {
  name: "PageTitle",
  props: {
    icon: {
      type: String,
      required: false,
      default: () => null,
    },
    primary: {
      type: String,
      required: true,
    },
    secondary: {
      type: String,
      required: true,
    },
  }
};
</script>
