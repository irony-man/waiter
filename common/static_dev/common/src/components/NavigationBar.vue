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
            class="btn d-flex gap-3 align-items-center btn-outline-primary"
            :to="{ name: 'table-cart', params: { tableUid: $route.params.tableUid } }">
            <i class="ci-cart"/><span class="d-none d-lg-block">{{ $filters.formatCurrency(totalPrice) }}</span>
          </router-link>
          <router-link
            v-if="$route.meta.showNavOrder"
            class="btn d-flex gap-3 align-items-center btn-primary"
            :to="{ name: 'table-order', params: { tableUid: $route.params.tableUid } }">
            <i class="fas fa-bowl-food"/><span class="d-none d-lg-block">Orders</span>
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
