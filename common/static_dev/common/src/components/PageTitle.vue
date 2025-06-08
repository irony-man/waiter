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
          class="letter-spacing-1 h3 fw-medium mb-1 text-uppercase"
          v-html="primary"/>
        <p
          class="mb-0 text-uppercase"
          v-html="secondary"/>
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
