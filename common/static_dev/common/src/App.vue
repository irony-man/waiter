<template>
  <Loader
    ref="loader">
    <div class="site">
      <div class="content">
        <router-view v-slot="{ Component, route }">
          <UserNavigationBar v-if="route.meta.userNavigationBar"/>
          <NavigationBar v-else/>
          <component :is="Component"/>
        </router-view>
      <!-- <Footer/> -->
      </div>
    </div>
  </Loader>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
import UserNavigationBar from "./components/UserNavigationBar.vue";
import Loader from "./components/Loader.vue";
import {mapActions} from "vuex";

export default {
  name: "App",
  components: {NavigationBar, UserNavigationBar, Loader},
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
