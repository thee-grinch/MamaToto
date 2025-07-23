// src/App.vue
<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <div v-if="!isAuthenticated" class="min-h-screen">
      <router-view />
    </div>
    
    <div v-else class="min-h-screen">
      <AppHeader />
      <div class="flex">
        <AppNavigation class="hidden md:block" />
        <main class="flex-1 p-4 md:p-6 lg:p-8">
          <div class="max-w-7xl mx-auto">
            <router-view />
          </div>
        </main>
      </div>
      <AppNavigation class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t" mobile />
    </div>
    
    <AlertMessage 
      v-if="userStore.error" 
      :message="userStore.error" 
      type="error"
      @close="userStore.clearError()"
    />
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useUserStore } from './stores/user'
import AppHeader from './components/common/AppHeader.vue'
import AppNavigation from './components/common/AppNavigation.vue'
import AlertMessage from './components/common/AlertMessage.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppNavigation,
    AlertMessage
  },
  setup() {
    const userStore = useUserStore()
    const isAuthenticated = computed(() => userStore.isAuthenticated)

    onMounted(() => {
      // Initialize authentication state on app load
      userStore.initializeAuth()
    })

    return {
      userStore,
      isAuthenticated
    }
  }
}
</script>
