<template>
  <section>
    <h4>Your Profile</h4>
    <q-list bordered seperator style="max-width: 250px">
      <q-item>
        <q-item-section>
          <q-item-label overline>Full Name:</q-item-label>
          <q-item-label>{{ user.full_name }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section>
          <q-item-label overline>Username:</q-item-label>
          <q-item-label>{{ user.username }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item>
        <q-btn @click="deleteAccount()" color="accent" label="Delete Account" />
      </q-item>
    </q-list>
  </section>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "ProfileView",
  created: function () {
    return this.$store.dispatch("viewMe");
  },
  computed: {
    ...mapGetters({ user: "stateUser" }),
  },
  methods: {
    ...mapActions(["deleteUser"]),
    async deleteAccount() {
      try {
        await this.deleteUser(this.user.id);
        await this.$store.dispatch("logOut");
        this.$router.push({ name: "home" });
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>