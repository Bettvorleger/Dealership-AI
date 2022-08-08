<template>
  <q-scroll-area class="fit">
    <q-list v-if="isLoggedIn">
      <q-item :to="{ name: 'home' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="home" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Home </q-item-section>
      </q-item>
      <q-separator />
      <q-item :to="{ name: 'status' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="fact_check" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Status </q-item-section>
      </q-item>
      <q-separator />
      <q-item :to="{ name: 'dashboard' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="dashboard" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Dashboard </q-item-section>
      </q-item>
      <q-separator />
    </q-list>
    <q-list v-else>
        <q-item :to="{ name: 'home' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="home" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Home </q-item-section>
      </q-item>
      <q-separator />
      <q-item :to="{ name: 'status' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="fact_check" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Status </q-item-section>
      </q-item>
      <q-separator />
      <q-item :to="{ name: 'register' }" active-class="mobile-link" clickable v-ripple>
        <q-item-section avatar>
          <q-icon name="how_to_reg" />
        </q-item-section>
        <q-item-section class="text-uppercase text-weight-medium"> Register </q-item-section>
      </q-item>
    </q-list>
  </q-scroll-area>
</template>

<script>
export default {};
</script>

<style>
</style>