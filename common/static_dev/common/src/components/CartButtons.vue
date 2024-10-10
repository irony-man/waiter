<template>
  <div
    class="btn-group max-w-150"
    role="group">
    <LoadingButton
      v-if="value && available"
      :is-loading="!!removing"
      class="btn-outline-dark"
      btn-icon="fas fa-minus"
      :disabled="!value"
      @click="$emit('remove')"/>

    <Button
      v-if="value && available"
      class="btn-outline-dark"
      disabled>
      {{ value }}
    </Button>

    <LoadingButton
      v-if="available"
      :is-loading="!!adding"
      class="btn-outline-dark"
      btn-icon="fas fa-plus"
      @click="$emit('add')">
      <span
        v-if="!value"
        class="ms-3 text-uppercase fw-bold">Add</span>
    </LoadingButton>
    <Button
      v-else
      class="btn-outline-danger"
      disabled>
      Unavailable
    </Button>
  </div>
</template>

<script>
import Button from "./Button.vue";
import LoadingButton from "./LoadingButton.vue";

export default {
  name: "CartButtons",
  components: { LoadingButton, Button },
  props: {
    value: {
      type: Number,
      required: true
    },
    available: {
      type: Boolean,
      required: false,
      default: true
    },
    adding: {
      type: Boolean,
      required: false,
      default: false
    },
    removing: {
      type: Boolean,
      required: false,
      default: false
    },
  },
  emits: ['remove', 'add']
};
</script>
