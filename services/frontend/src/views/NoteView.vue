<template>
  <q-list v-if="note" bordered seperator style="max-width: 250px">
    <q-item>
      <q-item-section>
        <q-item-label overline>Title</q-item-label>
        <q-item-label>{{ note.title }}</q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label overline>Content:</q-item-label>
        <q-item-label>{{ note.content }}</q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label overline>Author:</q-item-label>
        <q-item-label>{{ note.author.username }}</q-item-label>
      </q-item-section>
    </q-item>
    <div v-if="user.id === note.author.id" class="q-mt-md row">
      <q-item>
        <q-btn flat color="accent" @click="editNote()" label="Edit" />
      </q-item>
      <q-item>
        <q-btn flat color="accent" @click="removeNote()" label="Delete" />
      </q-item>
    </div>
  </q-list>
</template>


<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "NoteView",
  props: ["id"],
  async created() {
    try {
      await this.viewNote(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push({ name: "dashboard" });
    }
  },
  computed: {
    ...mapGetters({ note: "stateNote", user: "stateUser" }),
  },
  methods: {
    ...mapActions(["viewNote", "deleteNote"]),
    async removeNote() {
      try {
        await this.deleteNote(this.id);
        this.$router.push({ name: "dashboard" });
      } catch (error) {
        console.error(error);
      }
    },
    async editNote() {
      try {
        this.$router.push({ name: "editNote", params: { id: this.id } });
      } catch (error) {
        console.log("Note cannot be edited.");
      }
    },
  },
};
</script>