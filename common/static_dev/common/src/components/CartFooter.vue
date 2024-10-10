<template>
  <div
    class="btn-group btn-group-sm"
    role="group">
    <LoadingButton
      :is-loading="!!removing"
      class="btn-outline-dark"
      btn-icon="fas fa-minus"
      :disabled="!value"
      @click="$emit('remove')"/>

    <Button
      class="btn-outline-dark"
      disabled>
      {{ value }}
    </Button>

    <LoadingButton
      :is-loading="!!adding"
      class="btn-outline-dark"
      btn-icon="fas fa-plus"
      @click="$emit('add')"/>
  </div>
</template>

<script>
import Button from "./Button.vue";
import LoadingButton from "./LoadingButton.vue";

export default {
  name: "CartFooter",
  components: { LoadingButton, Button },
  props: {
    value: {
      type: Number,
      required: true
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
