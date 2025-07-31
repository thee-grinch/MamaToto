<template>
  <div id="app">
    <AppHeader />
    <AppNavigation />
    <router-view></router-view>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import AppNavigation from './AppNavigation.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppNavigation,
  },
};
</script>

<style>
/* Add your global styles here */
</style>