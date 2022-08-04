<template>
  <q-header height-hint="98">
    <q-toolbar class="bg-secondary text-black rounded-borders row">

      <router-link
        :to="{ name: 'home' }"
        class="col q-my-sm q-mr-lg q-ml-xs"
        align="left"
      >
        <q-img to="/home" src="@/assets/logo.png" style="width: 220px" />
      </router-link>

      <div v-if="isLoggedIn" class="col" align="center">
        <q-tabs>
          <q-route-tab :to="{ name: 'home' }" label="Home" />
          <q-route-tab :to="{ name: 'status' }" label="Status" />
          <q-route-tab :to="{ name: 'dashboard' }" label="Dashboard" />
        </q-tabs>
      </div>

      <div v-else class="col" align="center">
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
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch("logOut");
      this.$router.push({ name: "login" });
    },
  },
};
</script>

<style>
</style>