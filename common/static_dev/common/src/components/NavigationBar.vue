<template>
  <div class="shadow-sm mb-5">
    <div class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link
          class="navbar-brand d-none d-lg-block me-3 flex-shrink-0"
          :to="{ name: 'home' }">
          <img
            src="@/assets/images/logo.png"
            alt="Waiter"
            style="max-width: 80px;">
        </router-link>
        <router-link
          class="navbar-brand d-lg-none me-2"
          :to="{ name: 'home' }">
          <img
            src="@/assets/images/logo.png"
            alt="Waiter"
            style="max-width: 60px;">
        </router-link>
        <div class="navbar-toolbar d-flex gap-3 align-items-center">
          <router-link
            v-if="totalPrice && $route.meta.showNavCart"
            class="btn btn-outline-dark"
            :to="{ name: 'table-cart', params: { tableUid: $route.params.tableUid } }">
            <i class="fas fa-cart-shopping me-3"/> {{ $filters.formatCurrency(totalPrice) }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { mapState } from "vuex";

export default {
  name: "NavigationBar",
  computed: {
    ...mapState(["cart"]),
    totalPrice() {
      return Object.values(this.cart).reduce((sum, { quantity, price }) => sum + quantity * price, 0);
    }
  },
};
</script>
