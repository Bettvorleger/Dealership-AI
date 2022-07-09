<template>
  <div class="dai">
    <q-layout class="dai__layout" view="hHh lpR fFf">
      <NavBar class="dai__header shadow-3 rounded-borders" />
      <q-space />
      <q-page-container class="dai__page-container">
        <router-view class="dai__page shadow-3 rounded-borders" />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref, computed } from "vue";
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },

  setup() {
    const $q = useQuasar()

    const style = computed(() => ({
      height: $q.screen.height + 'px'
    }))

    return {
      leftDrawerOpen: ref(false),
      style
    };
  },
};
</script>
