<template>
  <div>
    <div
      v-for="(choice, i) in choices"
      :key="choice.value"
      class="form-check">
      <input
        :id="`${name}_${i}`"
        :value="choice.value.trim()"
        :name="name"
        :checked="choice.value.trim() === modelValue"
        :required="required"
        class="form-check-input"
        type="radio"
        @input="$emit('update:modelValue', $event.target.value)">
      <label
        :for="`${name}_${i}`"
        class="form-label onboarding-radio-label mb-2">
        {{ choice.name }}
      </label>
    </div>
    <div
      v-if="error && error.length"
      class="small text-danger mt-2">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Radio",
  props: {
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
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
      required: true,
    },
  },
};
</script>
