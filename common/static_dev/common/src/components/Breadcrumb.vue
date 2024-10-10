<template>
  <div class="breadcrumb mb-4">
    <router-link
      v-for="item in routerItems"
      :key="item.name"
      :to="item.to"
      class="breadcrumb-item">
      {{ item.name }}
    </router-link>
    <a class="breadcrumb-item active">
      {{ name }}
    </a>
  </div>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Breadcrumb",
  props: {
    routerItems: {
      type: Array,
      required: false,
      default: () => [],
    },
    name: {
      type: String,
      required: true,
    },
  },
};
</script>
