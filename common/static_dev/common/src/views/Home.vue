<template>
  <Loader ref="loader">
    <div
      class="container d-flex align-items-center justify-content-center"
      style="height: 70vh; max-width: 780px;">
      <div class="text-center">
        <div class="fs-1">
          Welcome to <strong>Waiter</strong>
        </div>
        <div class="my-4">
          The ultimate dining experience! Our platform allows you to easily order food directly from your table at your
          favorite restaurant by simply scanning a QR code. No more waiting for servers or handling physical menus—just
          scan, browse the digital menu, customize your order, and submit it instantly. Track your order in real time,
          request refills, and even pay—all from your smartphone! Enjoy a seamless, contactless, and efficient dining
          experience with Waiter. Your convenience is our priority!
        </div>
        <router-link
          class="btn btn-primary"
          :to="{ name: 'dashboard' }">
          Dashboard
        </router-link>
      </div>
    </div>
  </Loader>
</template>

<script>
import Loader from "@/components/Loader.vue";
import { mapState } from "vuex";

export default {
  name: "Home",
  components: { Loader },
  mounted() {
    this.$refs.loader.complete();
  },
  methods: {
    ...mapState(['user']),
  }
};
</script>
