<template>
  <section>
    <h4>Edit note</h4>

    <q-form @submit="submit" class="q-gutter-md">
      <q-input
        outlined
        color="black"
        type="text"
        name="title"
        label="Title"
        v-model="form.title"
        lazy-rules
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
      />
      <q-input
        outlined
        color="black"
        type="text"
        name="content"
        label="Content"
        v-model="form.content"
        autogrow
        lazy-rules
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
      />
      <q-btn type="submit" color="accent" label="Submit" />
    </q-form>
  </section>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "editNote",
  props: ["id"],
  data() {
    return {
      form: {
        title: "",
        content: "",
      },
    };
  },
  created: function () {
    this.getNote();
  },
  computed: {
    ...mapGetters({ note: "stateNote" }),
  },
  methods: {
    ...mapActions(["updateNote", "viewNote"]),
    async submit() {
      try {
        let note = {
          id: this.id,
          form: this.form,
        };
        await this.updateNote(note);
        this.$router.push({ name: "note", params: { id: this.note.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async getNote() {
      try {
        await this.viewNote(this.id);
        this.form.title = this.note.title;
        this.form.content = this.note.content;
      } catch (error) {
        console.error(error);
        this.$router.push({ name: "dashboard" });
      }
    },
  },
};
</script>