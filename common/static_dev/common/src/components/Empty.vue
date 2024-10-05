<template>
  <div
    class="d-flex align-items-center"
    :class="shadeClass()">
    <i
      class="fas fa-2x me-4"
      :class="icon"/>
    <div>
      <h6 class="fw-bold text-uppercase mb-1">
        {{ title }}
      </h6>
      <div
        class="small"
        v-html="text"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "Empty",
  props: {
    kind: {
      type: String,
      required: false,
      default: () => null
    },
    icon: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
  methods: {
    shadeClass() {
      if (this.kind && this.kind.length) {
        return `alert alert-${this.kind} p-4`;
      }

      return "alert alert-secondary p-4";
    },
  }
};
</script>
