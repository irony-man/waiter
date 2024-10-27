<template>
  <Loader ref="loader">
    <div class="container">
      <!-- Router view -->
      <router-view v-slot="{ Component }">
        <component :is="Component"/>
      </router-view>
    </div>
  </Loader>
</template>

<script>
import Loader from "@/components/Loader.vue";

export default {
  name: "Dashboard",
  components: {Loader},
  async mounted() {
    this.$refs.loader.complete();
  },
};
</script>
