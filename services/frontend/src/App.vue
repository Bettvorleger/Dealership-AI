<template>
  <div class="dai">
    <q-layout class="dai__layout" view="lHh lpR fFf">
      <NavBar
        class="dai__header shadow-3 rounded-borders"
        @clickDrawer="toggleLeftDrawer"
      />
      <q-drawer
        v-model="leftDrawerOpen"
        side="left"
        overlay
        behavior="mobile"
        class="bg-grey-3"
        :width="200"
        :breakpoint="500"
        bordered
      >
        <NavBarMobile />
      </q-drawer>
      <q-space />
      <q-page-container class="dai__page-container">
        <router-view class="dai__page shadow-3 rounded-borders" />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, computed } from "vue";
import NavBar from "@/components/NavBar.vue";
import NavBarMobile from "./components/NavBarMobile.vue";

export default {
  name: "App",
  components: {
    NavBar,
    NavBarMobile,
  },

  setup() {
    const $q = useQuasar();

    const style = computed(() => ({
      height: $q.screen.height + "px",
    }));

    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      style,
    };
  },
};
</script>
