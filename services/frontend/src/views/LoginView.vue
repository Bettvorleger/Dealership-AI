<template>
  <section>
    <q-card flat class="form-card">
      <q-card-section>
        <h4 class="text-center">Login to your account</h4>
        <q-form @submit="submit" class="q-gutter-md">
          <q-input
            outlined
            color="black"
            type="text"
            name="username"
            label="Username"
            v-model="form.username"
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
            v-model="form.password"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />
          <div class="row">
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
  name: "LoginView",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    ...mapActions(["logIn"]),
    async submit() {
      const User = new FormData();
      User.append("username", this.form.username);
      User.append("password", this.form.password);
      await this.logIn(User);
      this.$router.push({ name: "dashboard" });
    },
  },
};
</script>