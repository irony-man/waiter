<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required && label"
        class="ms-1">*</span></label>
    <div
      v-for="(choice, i) in choices"
      :key="choice.value">
      <input
        :id="`${name}_${i}`"
        :value="choice.value.trim()"
        :name="name"
        :checked="choice.value.trim() === modelValue"
        :required="required"
        class="btn-check"
        type="radio"
        @input="$emit('update:modelValue', $event.target.value)">
      <label
        :for="`${name}_${i}`"
        class="btn d-flex gap-3 justify-content-between btn-outline-primary text-start w-100 mb-3">
        <div>{{ choice.start }}</div>
        <div>{{ choice.end }}</div>
      </label>
    </div>
    <div
      v-if="helpText"
      class="small text-muted mt-1">
      {{ helpText }}
    </div>
    <Error :error="error"/>
  </div>
</template>

<script>
import Error from './Error.vue';

export default {
  name: "Radio",
  components: { Error },
  props: {
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: null
    },
    error: {
      type: String,
      required: false,
      default: () => '',
    },
    choices: {
      type: Array,
      required: true,
    },
    required: {
      type: Boolean,
      required: false,
      default: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
    helpText: {
      type: String,
      required: false,
      default: () => null,
    },
  },
  emits: ['update:modelValue'],
};
</script>
