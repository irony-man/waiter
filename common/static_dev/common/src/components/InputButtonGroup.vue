<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}</label>
    <div class="input-group">
      <input
        :id="name"
        ref="input"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        class="form-control"
        :value="modelValue"
        @blur="$emit('blur')"
        @input="onInput">
      <button
        class="btn btn-outline-primary"
        type="button"
        @click="$emit('clicked')">
        {{ btnText }}
      </button>
    </div>
    <div
      v-if="msg"
      class="small text-muted mt-1">
      {{ msg }}
    </div>
    <div
      v-if="error && error.length"
      class="small text-danger mt-1">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: "InputButtonGroup",
  props: {
    name: {
      type: String,
      required: true,
    },
    modelValue: {
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    btnText: {
      type: String,
      required: true,
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
  },
  emits: ['update:modelValue', 'blur', 'clicked'],
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
