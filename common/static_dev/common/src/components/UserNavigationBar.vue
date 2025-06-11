<template>
  <div class="shadow-sm mb-5">
    <div class="navbar navbar-expand-lg navbar-light">
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
            v-if="user.is_staff"
            class="ms-1 me-1 me-lg-5 nav-link"
            href="/wtr-adm/"
            target="_blank">
            <i class="fas fa-user me-2"/> Admin
          </a>
          <a
            class="nav-link"
            href="/logout/">
            <div class="mt-2">
              <i class="fas fa-right-from-bracket"/> Logout
            </div>
            <div class=" ms-n2"><small>Hi, {{ user.username }}
            </small></div>
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
