<template>
  <div class="form-check form-switch">
    <input
      :id="name"
      ref="input"
      type="checkbox"
      role="switch"
      :name="name"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      class="form-check-input"
      :value="modelValue"
      :checked="modelValue"
      @blur="$emit('blur')"
      @input="onInput">
    <label
      class="form-check-label"
      :for="name">{{ label }}<span
        v-if="required"
        class="ms-1">*</span></label>
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
  name: "Switch",
  components: {Error},
  props: {
    name: {
      type: String,
      required: true,
    },
    modelValue: {
      required: true,
      type: null
    },
    type: {
      type: String,
      required: false,
      default: 'text'
    },
    hideSpinButtons: {
      type: Boolean,
      required: false,
      default: false
    },
    label: {
      type: String,
      required: false,
      default: () => ''
    },
    addon: {
      type: String,
      required: false,
      default: () => ''
    },
    placeholder: {
      type: String,
      required: false,
      default: () => '',
    },
    helpText: {
      type: String,
      required: false,
      default: () => null,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    capitalize: {
      type: Boolean,
      required: false,
      default: false,
    },
    error: {
      type: String,
      required: false,
      default: '',
    },
    step: {
      type: String,
      required: false,
      default: () => undefined,
    },
    textCapitalize: {
      type: Boolean,
      required: false,
      default: false
    },
    min: {
      type: Number,
      required: false,
      default: null
    },
    max: {
      type: Number,
      required: false,
      default: null
    },
  },
  emits: ['update:modelValue', 'blur'],
  methods: {
    focus() {
      this.$refs.input.focus();
    },
    onInput(event) {
      this.$emit('update:modelValue', event.target.checked);
    }
  }
};
</script>

<style scoped>
.hide-spin-buttons::-webkit-inner-spin-button,
.hide-spin-buttons::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
