<template>
  <Loader ref="loader">
    <div class="container">
      <div
        class=" d-flex align-items-center justify-content-center"
        style="height: 70vh;">
        <div
          class="text-center"
          style="max-width: 780px;">
          <div class="fs-1 mb-3">
            Welcome to <strong class="text-primary">Waiter</strong>
          </div>
          <div class="mb-5">
            The ultimate dining experience! Our platform allows you to easily order food directly from your table at your
            favorite restaurant by simply scanning a QR code. No more waiting for servers or handling physical menus—just
            scan, browse the digital menu, customize your order, and submit it instantly. Enjoy a seamless, contactless, and efficient dining
            experience with <strong class="text-primary">Waiter</strong>. Your convenience is our priority!
          </div>
          <div class="d-flex justify-content-center gap-4">
            <Button
              class="btn-outline-primary"
              btn-icon="fas fa-qrcode me-2"
              @click="showScanner = true">
              Open Scanner
            </Button>
            <router-link
              class="btn btn-primary"
              :to="{ name: 'dashboard' }">
              Dashboard <i class="fas fa-arrow-right ms-2"/>
            </router-link>
          </div>
        </div>
      </div>
      <div class="w-450 mb-5 mx-auto">
        <ScannerModal
          v-if="showScanner"
          @scan="onScan"/>
      </div>
    </div>
  </Loader>
</template>

<script>
import Loader from "@/components/Loader.vue";
import ScannerModal from "../components/ScannerModal.vue";
import Button from "../components/Button.vue";

export default {
  name: "Home",
  components: { Loader, ScannerModal, Button },
  data() {
    return {
      showScanner: false,
    };
  },
  mounted() {
    this.$refs.loader.complete();
  },
  methods: {
    onScan(text) {
      this.showScanner = false;
      window.location = text;
    }
  }
};
</script>
