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
        <div
          v-if="!!user.uid"
          class="navbar-toolbar d-flex gap-3 align-items-center">
          <a
            class="navbar-tool fw-bold ms-1 ms-lg-0 me-n1 me-lg-2"
            href="/wtr-adm/"
            target="_blank">
            <div class="navbar-tool-icon-box">
              <i class="navbar-tool-icon ci-user"/>
            </div>
            <div class="navbar-tool-text ms-n2">Admin</div>
          </a>
          <a
            class="navbar-tool ms-1 ms-lg-0 me-n1 me-lg-2"
            href="/logout/">
            <div class="navbar-tool-icon-box mt-2">
              <i class="navbar-tool-icon fas fa-right-from-bracket"/>
            </div>
            <div class="navbar-tool-text ms-n2"><small>Hello, {{ user.username }}
            </small>Logout</div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { mapState } from "vuex";

export default {
  name: "UserNavigationBar",
  computed: {
    ...mapState(["user"]),
  },
};
</script>
