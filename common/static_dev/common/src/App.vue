<template>
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
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
import UserNavigationBar from "./components/UserNavigationBar.vue";
import Footer from "./components/Footer.vue";
import { mapActions } from "vuex";

export default {
  name: "App",
  components: {NavigationBar, UserNavigationBar, Footer},
  async mounted() {
    await this.getCart();
  },
  methods: {
    ...mapActions(['getCart']),
  },
};
</script>
