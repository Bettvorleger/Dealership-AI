<template>
  <q-header height-hint="98">
    <q-toolbar class="bg-secondary text-black rounded-borders row wrap">
      <q-btn flat round icon="menu" class="q-mr-md self-center" id="mobile-nav" @click="toggleLeftDrawer" />
      <router-link
        :to="{ name: 'home' }"
        class="col q-my-sm q-mr-lg q-ml-xs"
        align="left"
      >
        <q-img to="/home" src="@/assets/logo.png" style="max-width: 220px" />
      </router-link>

      <div v-if="isLoggedIn" id="desktop-nav" class="col" align="center">
        <q-tabs>
          <q-route-tab :to="{ name: 'home' }" label="Home" />
          <q-route-tab :to="{ name: 'status' }" label="Status" />
          <q-route-tab :to="{ name: 'dashboard' }" label="Dashboard" />
        </q-tabs>
      </div>

      <div v-else class="col" id="desktop-nav" align="center">
        <q-tabs>
          <q-route-tab :to="{ name: 'home' }" label="Home" />
          <q-route-tab :to="{ name: 'status' }" label="Status" />
          <q-route-tab :to="{ name: 'register' }" label="Register" />
        </q-tabs>
      </div>

      <div v-if="isLoggedIn" class="col q-mr-xs" align="right">
        <q-btn flat round icon="person" to="/profile" />
        <q-btn flat round icon="logout" @click="logout" />
      </div>
      <div v-else class="col q-mr-xs" align="right">
        <q-btn flat round icon="login" to="/login" />
      </div>
    </q-toolbar>
  </q-header>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    // get auth store entry for login
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    // click action for logout
    async logout() {
      await this.$store.dispatch("logOut");
      this.$router.push({ name: "login" });
    },
    // click action for mobile hamburger menu for parent component
    toggleLeftDrawer() {
      this.$emit('clickDrawer', 'click')
    }
  },
};
</script>

<style>
</style>