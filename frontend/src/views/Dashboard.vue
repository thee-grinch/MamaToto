<!-- src/views/Dashboard.vue -->
<template>
  <div class="space-y-6">
    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
      <h1 class="text-2xl md:text-3xl font-bold">
        Welcome back, {{ userStore.user?.first_name || 'Mama' }}! 👋
      </h1>
      <p class="mt-2 text-pink-100">
        Here's your health overview for today
      </p>
    </div>

    <!-- Loading State -->
    <LoadingSpinner v-if="healthStore.loading" size="large" message="Loading your dashboard..." />

    <!-- Dashboard Content -->
    <div v-else-if="dashboardData" class="space-y-6">
      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Active Pregnancy"
          :value="dashboardData.active_pregnancy ? `Week ${dashboardData.active_pregnancy.current_week || 'N/A'}` : 'None'"
          icon="heart"
          color="pink"
        />
        <StatCard
          title="Children"
          :value="dashboardData.children?.length || 0"
          icon="users"
          color="blue"
        />
        <StatCard
          title="Upcoming Appointments"
          :value="dashboardData.upcoming_appointments?.length || 0"
          icon="calendar"
          color="green"
        />
        <StatCard
          title="Overdue Vaccinations"
          :value="dashboardData.overdue_vaccinations?.length || 0"
          icon="alert"
          color="red"
        />
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Active Pregnancy Card -->
          <PregnancyOverviewCard 
            v-if="dashboardData.active_pregnancy"
            :pregnancy="dashboardData.active_pregnancy"
          />

          <!-- Children Overview -->
          <ChildrenOverviewCard 
            v-if="dashboardData.children?.length > 0"
            :children="dashboardData.children"
          />

          <!-- Recent Health Records -->
          <HealthRecordsCard 
            v-if="dashboardData.recent_health_records?.length > 0"
            :records="dashboardData.recent_health_records"
          />
        </div>

        <!-- Right Column -->
        <div class="space-y-6">
          <!-- Alerts and Notifications -->
          <AlertsCard 
            :overdue-vaccinations="dashboardData.overdue_vaccinations || []"
            :growth-alerts="dashboardData.growth_alerts || []"
          />

          <!-- Upcoming Appointments -->
          <AppointmentsCard 
            :appointments="dashboardData.upcoming_appointments || []"
          />

          <!-- Quick Actions -->
          <QuickActionsCard />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No data available</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by adding your health information.</p>
      <div class="mt-6">
        <router-link
          to="/pregnancy"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-pink-600 hover:bg-pink-700"
        >
          Get Started
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useHealthStore } from '../stores/health'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

// Import dashboard components
import StatCard from '../components/dashboard/StatCard.vue'
import PregnancyOverviewCard from '../components/dashboard/PregnancyOverviewCard.vue'
import ChildrenOverviewCard from '../components/dashboard/ChildrenOverviewCard.vue'
import HealthRecordsCard from '../components/dashboard/HealthRecordsCard.vue'
import AlertsCard from '../components/dashboard/AlertsCard.vue'
import AppointmentsCard from '../components/dashboard/AppointmentsCard.vue'
import QuickActionsCard from '../components/dashboard/QuickActionsCard.vue'

export default {
  name: 'Dashboard',
  components: {
    LoadingSpinner,
    StatCard,
    PregnancyOverviewCard,
    ChildrenOverviewCard,
    HealthRecordsCard,
    AlertsCard,
    AppointmentsCard,
    QuickActionsCard
  },
  setup() {
    const userStore = useUserStore()
    const healthStore = useHealthStore()
    
    const dashboardData = computed(() => healthStore.dashboardData)
    
    onMounted(() => {
      healthStore.fetchDashboardData()
    })
    
    return {
      userStore,
      healthStore,
      dashboardData
    }
  }
}
</script>