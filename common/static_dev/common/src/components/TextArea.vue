<template>
  <div class="form-group">
    <label
      v-if="label"
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required && label"
        class="ms-1">*</span></label>
    <textarea
      :id="name"
      :value="modelValue"
      :name="name"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :rows="rows"
      class="form-control"
      @change="e => $emit('update:modelValue', e.target.value)"/>
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
  name: "TextArea",
  components: { Error },
  props: {
    name: {
      type: String,
      required: false,
      default: () => 'text-area'
    },
    modelValue: {
      required: true,
      type: null
    },
    label: {
      type: String,
      required: false,
      default: () => null
    },
    placeholder: {
      type: String,
      required: false,
      default: () => null,
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
    error: {
      type: String,
      required: false,
      default: '',
    },
    rows: {
      type: [String, Number],
      required: false,
      default: () => 5
    },
  },
  emits: ['update:modelValue'],
};
</script>
