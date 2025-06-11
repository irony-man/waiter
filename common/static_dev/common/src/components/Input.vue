<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required && label"
        class="ms-1">*</span></label>
    <div class="position-relative">
      <input
        :id="name"
        ref="input"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :min="min"
        :max="max"
        class="form-control shadow-sm"
        :step="step ? step : undefined"
        :class="{ 'hide-spin-buttons': hideSpinButtons, 'text-capitalize': textCapitalize, 'ps-5': icon, 'form-control-sm': size === 'sm', 'form-control-lg': size === 'lg' }"
        :value="modelValue"
        @blur="$emit('blur')"
        @input="onInput">
      <div
        v-if="icon"
        class="position-absolute top-50 start-0 translate-middle-y ps-3">
        <i
          :class="icon"
          class="text-muted"/>
      </div>
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
  name: "Input",
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
      default: true,
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
    icon: {
      type: String,
      required: false,
      default: () => ''
    },
    size: {
      type: String,
      required: false,
      default: () => ''
    }
  },
  emits: ['update:modelValue', 'blur'],
  methods: {
    focus() {
      this.$refs.input.focus();
    },
    onInput(event) {
      let value = event.target.value;
      if (this.capitalize && value && value.toUpperCase) {
        value = value.toUpperCase();
      }
      this.$emit('update:modelValue', value);
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
