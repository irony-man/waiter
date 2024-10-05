<template>
  <div>
    <div
      v-if="isLoading"
      class="text-center">
      <div
        class="mt-4 spinner-border text-primary"
        role="status"/>
    </div>
    <slot v-else/>
  </div>
</template>

<script>
export default {
  name: "Loader",
  data() {
    return {
      isLoading: true,
    };
  },
  methods: {
    complete() {
      // Too quick loading completion can be jarring.
      // window.setTimeout(() => {
      //   this.isLoading = false;
      // }, 250);
      this.isLoading = false;
    },
    start() {
      this.isLoading = true;
    },
  },
};
</script>
