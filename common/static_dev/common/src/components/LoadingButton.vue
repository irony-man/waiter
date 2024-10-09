<template>
  <button
    :type="btnType"
    class="btn btn-icon"
    :disabled="isLoading || disabled">
    <span v-if="isLoading">
      <span class="spinner-border spinner-border-sm me-1"/>&nbsp;
    </span>
    <span v-else>
      <i
        v-if="btnIcon"
        class="me-2"
        :class="btnIcon"/>
    </span>
    <slot/>
  </button>
</template>

<script>
export default {
  name: "LoadingButton",
  props: {
    btnType: {
      type: String,
      required: false,
      default: 'button',
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    btnIcon: {
      type: String,
      required: false,
      default: ""
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    }
  },
};
</script>
