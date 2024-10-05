<template>
  <div
    v-if="error"
    class="text-danger small mt-1">
    <span v-if="Array.isArray(error) && error.length">
      {{ error.join(' ') }}
    </span>
    <span v-else-if="error">
      {{ error }}
    </span>
  </div>
</template>

<script>
export default {
  name: "Error",
  props: {
    error: {
      type: String || Array || null || undefined,
      required: false,
      default: '',
    },
  },
};
</script>
