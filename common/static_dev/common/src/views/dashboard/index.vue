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
import { mapActions } from "vuex";
import Loader from "@/components/Loader.vue";

export default {
  name: "Dashboard",
  components: {Loader},
  async mounted() {
    try {
      await this.getUser();
    } catch (error) {
      this.$toast.error("Error fetching user");
    }
    this.$refs.loader.complete();
  },
  methods: {
    ...mapActions(['getUser']),
  },
};
</script>
