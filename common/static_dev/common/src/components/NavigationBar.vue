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
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "NavigationBar",
};
</script>
