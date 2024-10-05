<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required"
        class="ms-1">*</span></label>
    <div class="input-group">
      <div
        v-if="addon"
        :id="name"
        class="input-group-text"
        v-html="addon"/>
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
        class="form-control"
        :step="step ? step : undefined"
        :class="{ 'hide-spin-buttons': hideSpinButtons, 'text-capitalize': textCapitalize }"
        :value="modelValue"
        @blur="$emit('blur')"
        @input="onInput">
    </div>
    <div
      v-if="msg"
      class="small text-muted mt-1">
      {{ msg }}
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
  },
  emits: ['update:modelValue', 'blur'],
  computed: {
    msg() {
      if (this.helpText) {
        if (!this.required) {
          return `Optional - ${this.helpText}`;
        } else {
          return this.helpText;
        }
      }

      if (!this.required) {
        return "Optional";
      }

      return null;
    }
  },
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
