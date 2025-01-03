<template>
  <!-- Tabs navs -->
  <ul
    class="nav nav-tabs nav-justified"
    role="tablist">
    <li
      v-for="tab in tabs"
      :key="tab.value"
      class="nav-item"
      role="presentation">
      <button
        class="nav-link"
        :class="modelValue === tab.value ? 'active':''"
        type="button"
        role="tab"
        @click="() => $emit('update:modelValue', tab.value)">
        {{ tab.name }}
      </button>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'Tabs',
  props: {
    tabs: {
      type: Array,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue']
};
</script>
