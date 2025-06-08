<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required && label"
        class="ms-1">*</span></label>
    <select
      :id="name"
      :value="modelValue"
      :name="name"
      :required="required"
      class="form-select shadow-sm"
      :disabled="disabled"
      @input="$emit('update:modelValue', $event.target.value)">
      <option
        :value="null"
        hidden
        disabled>
        Select a choice
      </option>
      <option
        v-for="choice in choices"
        :key="choice[trackBy]"
        :value="choice[trackBy]">
        <span v-if="renders.length">
          {{ renders.map((line) => recursiveGet(choice, line)).join(' :: ') }}
        </span>
        <span v-else>
          {{ choice[displayBy] }}
        </span>
      </option>
    </select>
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
  name: "Select",
  components: { Error },
  props: {
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    choices: {
      type: Array,
      required: true,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    modelValue: {
      required: true,
      type: [String, Number, Boolean, Object, Array],
    },
    placeholder: {
      type: String,
      required: false,
      default: ''
    },
    error: {
      type: String || Array || null || undefined,
      required: false,
      default: () => null
    },
    disabled: {
      required: false,
      default: false,
      type: Boolean,
    },
    helpText: {
      type: String,
      required: false,
      default: () => null,
    },
    trackBy: {
      type: String,
      required: false,
      default: 'value'
    },
    displayBy: {
      type: String,
      required: false,
      default: 'name'
    },
    renders: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  emits: ['update:modelValue'],
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
};
</script>
