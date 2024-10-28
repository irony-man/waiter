<template>
  <div>
    <label
      :for="name"
      class="form-label">{{ label }}</label>
    <VueDatePicker
      :id="name"
      ref="datePickerComponent"
      v-model="localDate"
      :name="name"
      :required="required"
      :is-24="false"
      :placeholder="placeholder"
      :format="format"
      :text-input="textInput"
      month-name-format="long"
      :auto-apply="mode === 'date' ? true : false"
      :enable-time-picker="mode === 'date' ? false : true"
      @keydown.enter.prevent/>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

export default {
  name: 'DatePicker',
  components: {VueDatePicker},
  props: {
    name: {
      type: String,
      required: true,
    },
    modelValue: {
      required: true,
      type: Date,
    },
    label: {
      type: String,
      required: true,
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
    error: {
      type: String,
      required: false,
      default: '',
    },
    mode: {
      type: String,
      required: false,
      default: 'date',
    },
    placeholder: {
      type: String,
      required: false,
      default: null,
    },
    textInput: {
      type: Object,
      required: false,
      default: () => {}
    }
  },
  emits: ['update:modelValue'],
  computed: {
    localDate: {
      get() {
        return this.modelValue;
      },
      set(v) {
        var tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
        var localISOTime = (new Date(v - tzoffset)).toISOString().slice(0, -1);
        const finalValue = localISOTime.substring(0, 10);
        this.$emit('update:modelValue', finalValue);
      },
    },
    format() {
      return this.mode === 'date' ? 'dd-MM-yyyy' : 'yyyy-MM-dd hh:mm aa';
    },
  },
};
</script>
