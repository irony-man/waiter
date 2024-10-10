<template>
  <button
    :type="type"
    class="btn">
    <i
      v-if="btnIcon"
      :class="btnIcon"/>
    <slot/>
  </button>
</template>

<script>
export default {
  name: "LoadingButton",
  props: {
    type: {
      type: String,
      required: false,
      default: 'button',
    },
    btnText: {
      type: String,
      required: false,
      default: ""
    },
    btnIcon: {
      type: String,
      required: false,
      default: ""
    },
  },
};
</script>
