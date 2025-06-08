<template>
  <div class="form-group">
    <label
      :for="name"
      class="d-block form-label">{{ label }}<span
        v-if="required && label"
        class="ms-1">*</span></label>
    <Multiselect
      :id="name"
      :key="choices"
      :model-value="modelValue"
      :name="name"
      :placeholder="placeholder"
      open-direction="bottom"
      class="shadow-sm"
      :label="displayBy"
      :track-by="trackBy"
      :show-labels="false"
      :options="choices"
      :multiple="multiple"
      :searchable="true"
      :loading="isLoading"
      :internal-search="internalSearch"
      :disabled="disabled"
      @select="onSelect"
      @update:model-value="v => $emit('update:modelValue', v)"
      @search-change="search">
      <!-- eslint-disable-->
        <template #option="props">
          <div class="mb-1">
            <span v-if="renders.length">
              {{ renders.map((line) => recursiveGet(props.option, line)).join(' :: ') }}
            </span>
            <span v-else>
            {{ props.option[displayBy] }}
          </span>
          </div>
        </template>
        <template #singleLabel="props">
          <div>
            <span v-if="renders.length">
              {{ renders.map((line) => recursiveGet(props.option, line)).join(' :: ') }}
            </span>
            <span v-else>
              {{ props.option[displayBy] ?? props.option }}
          </span>
          </div>
        </template>
        <template v-slot:noOptions>
          <span>Type to search</span>
        </template>
        <template v-if="showClear" #clear>
          <span class="select-cross text-muted" @click.prevent="removeSelected">
            <i class="fa-solid fa-xmark"></i>
          </span>
        </template>
    </Multiselect>
    <div
      v-if="msg"
      class="small text-muted mt-1">
      {{ msg }}
    </div>
    <Error :error="error"/>
  </div>
</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<script>
import Multiselect from 'vue-multiselect';
import Error from './Error.vue';

export default {
  name: "ApiSelect",
  components: { Multiselect, Error },
  props: {
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    source: {
      type: Object,
      required: true,
    },
    placeholder: {
      type: String,
      required: false,
      default: ''
    },
    modelValue: {
      required: true,
      type: null,
    },
    labelClass: {
      type: String,
      required: false,
      default: '',
    },
    error: {
      type: String || Array || null || undefined,
      required: false,
      default: () => null
    },
    required: {
      type: Boolean,
      default: false,
      required: false,
    },
    disabled: {
      required: false,
      default: false,
      type: Boolean,
    },
    formText: {
      type: String,
      required: false,
      default: null,
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
    queryKey: {
      type: String,
      required: false,
      default: 'search',
    },
    internalSearch: {
      type: Boolean,
      default: false,
      required: false,
    },
    multiple: {
      type: Boolean,
      required: false,
      default: false
    },
    helpText: {
      type: String,
      required: false,
      default: () => null,
    },
    renders: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  emits: ['update:modelValue', 'input', 'select'],
  data() {
    return {
      choices: [],
      isLoading: false,
      searchReq: null,
    };
  },
  computed: {
    showClear() {
      if(this.multiple)
        return false;
      if(this.modelValue)
        return true;
      return false;
    },
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
  watch: {
    source(obj) {
      if (obj.array) {
        this.choices = obj.array;
      }
    },
  },
  $emits: ['select'],
  mounted() {
    console.log(this.modelValue, this.choices);

    if (this.source.array) {
      this.choices = this.source.array;
    }

  },
  methods: {
    async search(query) {
      if (!this.source.fetchFunction) {
        return;
      }

      if (!query || !query.length) {
        return;
      }

      if (this.searchReq) {
        window.clearTimeout(this.searchReq);
      }

      this.choices = [];
      this.searchReq = window.setTimeout(async () => {
        this.isLoading = true;
        let result = await this.source.fetchFunction({
          [this.queryKey]: query,
          ...this.source.params,
        });
        this.choices = result.results;
        this.isLoading = false;
      }, 300);
    },

    onSelect(v) {
      this.$emit('select', v);
    },
    removeSelected(e) {
      e.stopPropagation();
      this.$emit('update:modelValue', undefined);
    }
  }
};
</script>
