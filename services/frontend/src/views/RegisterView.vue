<template>
  <section>
    <q-card flat class="form-card">
      <q-card-section>
        <h4 class="text-center">Register your account</h4>
        <q-form @submit="submit" class="q-gutter-md">
          <q-input
            outlined
            color="black"
            type="text"
            name="username"
            label="Username"
            v-model="user.username"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />
          <q-input
            outlined
            color="black"
            type="text"
            name="full_name"
            label="Full Name"
            v-model="user.full_name"
            hint="Name and surname"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />
          <q-input
            outlined
            color="black"
            type="password"
            name="password"
            label="Password"
            v-model="user.password"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />
          <div class="row">
            <p v-if="error" class="col-sm-10 offset-md-1 text-negative text-center">{{ error }}</p>
            <q-btn
              class="col-sm-4 offset-md-4"
              type="submit"
              color="accent"
              label="Submit"
              align="center"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </section>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "RegisterView",
  data() {
    return {
      user: {
        username: "",
        full_name: "",
        password: "",
      },
      error: ""
    };
  },
  methods: {
    ...mapActions(["register"]),
    async submit() {
      try {
        await this.register(this.user);
        this.$router.push({ name: "dashboard" });
      } catch (error) {
        this.error = "Username already exists. Please try again.";
        throw 'Username already exists. Please try again.';
      }
    },
  },
};
</script>