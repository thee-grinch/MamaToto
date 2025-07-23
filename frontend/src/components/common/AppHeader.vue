<!-- src/components/common/AppHeader.vue -->
<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and title -->
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <h1 class="text-2xl font-bold text-pink-600">Mamatoto</h1>
          </div>
          <div class="hidden md:block ml-8">
            <nav class="flex space-x-8">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.to"
                class="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="{ 'text-pink-600 font-semibold': $route.name === item.name }"
              >
                {{ item.label }}
              </router-link>
            </nav>
          </div>
        </div>

        <!-- User menu -->
        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <button class="p-2 text-gray-400 hover:text-gray-500 relative">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 17h5l-5-5-5 5h5zm0 0v-5a4 4 0 00-8 0v5" />
            </svg>
            <span v-if="notificationCount > 0" 
                  class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
              {{ notificationCount }}
            </span>
          </button>

          <!-- User avatar and menu -->
          <div class="relative" ref="userMenuRef">
            <button 
              @click="toggleUserMenu"
              class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500"
            >
              <div class="h-8 w-8 rounded-full bg-pink-500 flex items-center justify-center text-white font-medium">
                {{ userStore.initials || 'U' }}
              </div>
              <span class="ml-2 text-gray-700 hidden sm:block">{{ userStore.fullName || 'User' }}</span>
              <svg class="ml-1 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- Dropdown menu -->
            <div v-show="showUserMenu" 
                 class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200">
              <router-link to="/profile" 
                          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Profile Settings
              </router-link>
              <button @click="logout" 
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useHealthStore } from '../../stores/health'

export default {
  name: 'AppHeader',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const healthStore = useHealthStore()
    
    const showUserMenu = ref(false)
    const userMenuRef = ref(null)
    
    const navigation = [
      { name: 'Dashboard', label: 'Dashboard', to: '/' },
      { name: 'Pregnancy', label: 'Pregnancy', to: '/pregnancy' },
      { name: 'Children', label: 'Children', to: '/children' },
      { name: 'HealthRecords', label: 'Health', to: '/health' },
      { name: 'Chatbot', label: 'Chat', to: '/chat' }
    ]
    
    const notificationCount = computed(() => {
      // Calculate notification count from dashboard data
      if (!healthStore.dashboardData) return 0
      
      const overdueVaccinations = healthStore.dashboardData.overdue_vaccinations?.length || 0
      const upcomingAppointments = healthStore.dashboardData.upcoming_appointments?.length || 0
      const growthAlerts = healthStore.dashboardData.growth_alerts?.length || 0
      
      return overdueVaccinations + upcomingAppointments + growthAlerts
    })
    
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const closeUserMenu = (event) => {
      if (!userMenuRef.value?.contains(event.target)) {
        showUserMenu.value = false
      }
    }
    
    const logout = async () => {
      userStore.logout()
      await router.push('/login')
    }
    
    onMounted(() => {
      document.addEventListener('click', closeUserMenu)
      healthStore.fetchDashboardData()
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', closeUserMenu)
    })
    
    return {
      userStore,
      navigation,
      showUserMenu,
      userMenuRef,
      notificationCount,
      toggleUserMenu,
      logout
    }
  }
}
</script>