<template>
  <div class="site">
    <div class="content">
      <NavigationBar/>
      <router-view/>
      <!-- <Footer/> -->
    </div>
  </div>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {NavigationBar,Footer},
};
</script>
