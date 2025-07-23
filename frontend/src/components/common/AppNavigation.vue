
<!-- src/components/common/AppNavigation.vue -->
<template>
  <nav :class="navigationClasses">
    <div class="px-4 py-6" v-if="!mobile">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Navigation</h2>
    </div>
    
    <div :class="mobile ? 'flex justify-around py-2' : 'px-4 space-y-2'">
      <router-link
        v-for="item in navigationItems"
        :key="item.name"
        :to="item.to"
        :class="[
          mobile ? 'flex flex-col items-center p-2 text-xs' : 'flex items-center px-3 py-2 text-sm font-medium rounded-lg',
          isActiveRoute(item.name) 
            ? (mobile ? 'text-pink-600' : 'bg-pink-100 text-pink-700')
            : (mobile ? 'text-gray-600' : 'text-gray-700 hover:bg-gray-100')
        ]"
      >
        <component :is="item.icon" :class="mobile ? 'h-5 w-5 mb-1' : 'h-5 w-5 mr-3'" />
        <span>{{ item.label }}</span>
        
        <!-- Badge for notifications -->
        <span v-if="item.badge && item.badge > 0" 
              :class="mobile ? 'absolute -mt-6 -mr-2' : 'ml-auto'"
              class="bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-5 h-5 flex items-center justify-center">
          {{ item.badge }}
        </span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useHealthStore } from '../../stores/health'

// Icon components (you can replace with actual icon library)
const DashboardIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
  </svg>`
}

const PregnancyIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
  </svg>`
}

const ChildrenIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>`
}

const HealthIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>`
}

const ChatIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>`
}

export default {
  name: 'AppNavigation',
  props: {
    mobile: {
      type: Boolean,
      default: false
    }
  },
  components: {
    DashboardIcon,
    PregnancyIcon,
    ChildrenIcon,
    HealthIcon,
    ChatIcon
  },
  setup(props) {
    const route = useRoute()
    const healthStore = useHealthStore()
    
    const navigationClasses = computed(() => {
      return props.mobile 
        ? 'bg-white border-t border-gray-200' 
        : 'w-64 bg-white shadow-sm h-screen'
    })
    
    const navigationItems = computed(() => {
      const dashboardData = healthStore.dashboardData
      
      return [
        {
          name: 'Dashboard',
          label: 'Dashboard',
          to: '/',
          icon: 'DashboardIcon',
          badge: 0
        },
        {
          name: 'Pregnancy',
          label: 'Pregnancy',
          to: '/pregnancy',
          icon: 'PregnancyIcon',
          badge: dashboardData?.upcoming_appointments?.length || 0
        },
        {
          name: 'Children',
          label: 'Children',
          to: '/children',
          icon: 'ChildrenIcon',
          badge: dashboardData?.overdue_vaccinations?.length || 0
        },
        {
          name: 'HealthRecords',
          label: 'Health',
          to: '/health',
          icon: 'HealthIcon',
          badge: dashboardData?.growth_alerts?.length || 0
        },
        {
          name: 'Chatbot',
          label: 'Chat',
          to: '/chat',
          icon: 'ChatIcon',
          badge: 0
        }
      ]
    })
    
    const isActiveRoute = (routeName) => {
      return route.name === routeName
    }
    
    return {
      navigationClasses,
      navigationItems,
      isActiveRoute
    }
  }
}
</script>