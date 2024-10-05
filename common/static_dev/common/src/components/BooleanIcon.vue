<template>
  <div
    class="is-20 p-1 d-flex flex-column justify-content-center align-items-center text-light rounded-circle"
    :class="value ? 'bg-success':'bg-danger'">
    <i
      class="fas"
      :class="value ? 'fa-check':'fa-xmark'"/>
  </div>
</template>

<script>
export default {
  name: "BooleanIcon",
  props: {
    value: {
      type: Boolean,
      required: false,
      default: () => false,
    },
  }
};
</script>
