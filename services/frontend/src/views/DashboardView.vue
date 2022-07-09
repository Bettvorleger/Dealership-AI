<template>
  <div>
    <section>
      <h4>Add new note</h4>

      <q-form @submit="submit">
        <div class="q-gutter-md" style="max-width:350px">
          <q-input
            outlined
            color="black"
            type="text"
            name="title"
            label="Title"
            v-model="form.title"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
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
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />
        </div>
        <q-btn type="submit" color="accent" label="Submit" />
      </q-form>
    </section>

    <br /><br />

    <section>
      <h4>Notes</h4>

      <div v-if="notes.length" class="q-pa-md row items-start q-gutter-md">
        <div v-for="note in notes" :key="note.id" class="notes">
          <q-card flat bordered>
            <q-card-section horizontal>
              <q-card-section class="q-pt-xs">
                <div class="text-overline">By {{ note.author.username }}</div>
                <div class="text-h5 q-mt-sm q-mb-xs">{{ note.title }}</div>
              </q-card-section>
            </q-card-section>
            <q-separator />

            <q-card-actions>
              <q-btn flat color="accent" @click="viewNote(note.id)">View</q-btn>
            </q-card-actions>
          </q-card>
          <br />
        </div>
      </div>

      <div v-else>
        <p>Nothing to see. Check back later.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "DashboardView",
  data() {
    return {
      form: {
        title: "",
        content: "",
      },
    };
  },
  created: function () {
    return this.$store.dispatch("getNotes");
  },
  computed: {
    ...mapGetters({ notes: "stateNotes" }),
  },
  methods: {
    ...mapActions(["createNote"]),
    async submit() {
      await this.createNote(this.form);
    },
    async viewNote(noteId) {
      console.log(noteId);
      try {
        this.$router.push({ name: "note", params: { id: noteId } });
      } catch (error) {
        console.log("Note cannot be opened.");
      }
    },
  },
};
</script>