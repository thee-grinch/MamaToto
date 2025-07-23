<!-- src/views/PregnancyTracker.vue -->
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Pregnancy Tracker</h1>
        <p class="mt-1 text-sm text-gray-500">Monitor your pregnancy journey</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button
          v-if="!pregnancyStore.activePregnancy"
          @click="showCreateForm = true"
          class="btn btn-primary"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Start Pregnancy Tracking
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <LoadingSpinner v-if="pregnancyStore.loading" size="large" message="Loading pregnancy data..." />

    <!-- Active Pregnancy -->
    <div v-else-if="pregnancyStore.activePregnancy" class="space-y-6">
      <!-- Current Week Card -->
      <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-3xl font-bold">Week {{ pregnancyStore.currentWeek || 'N/A' }}</h2>
            <p class="text-pink-100">Trimester {{ pregnancyStore.trimester || 'N/A' }}</p>
          </div>
          <div class="text-right">
            <p class="text-lg font-semibold">{{ weeksRemaining }} weeks to go</p>
            <p class="text-pink-100">Due: {{ formatDate(pregnancyStore.dueDate) }}</p>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm font-medium">
            <span>Progress</span>
            <span>{{ Math.round(progressPercentage) }}%</span>
          </div>
          <div class="w-full bg-pink-300 rounded-full h-3 mt-1">
            <div 
              class="bg-white h-3 rounded-full transition-all duration-300"
              :style="{ width: `${progressPercentage}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Weekly Information -->
      <WeeklyInfoCard 
        v-if="pregnancyStore.weeklyInfo"
        :weekly-info="pregnancyStore.weeklyInfo"
      />

      <!-- Quick Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-blue-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Last Weight</p>
              <p class="text-2xl font-semibold text-gray-900">
                {{ pregnancyStore.activePregnancy.last_weight || 'N/A' }} kg
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Last Checkup</p>
              <p class="text-lg font-semibold text-gray-900">
                {{ formatDate(pregnancyStore.activePregnancy.last_checkup) || 'Not recorded' }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-purple-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Next Appointment</p>
              <p class="text-lg font-semibold text-gray-900">
                {{ nextAppointmentDate || 'None scheduled' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Appointments and Tips -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Appointments -->
        <AppointmentsCard 
          :appointments="pregnancyStore.upcomingAppointments"
          @create-appointment="showAppointmentForm = true"
        />

        <!-- Health Tips -->
        <HealthTipsCard 
          v-if="pregnancyStore.weeklyInfo"
          :tips="pregnancyStore.weeklyInfo.tips"
          :week="pregnancyStore.currentWeek"
        />
      </div>

      <!-- Danger Signs Alert -->
      <DangerSignsCard 
        v-if="pregnancyStore.dangerSigns.length > 0"
        :danger-signs="pregnancyStore.dangerSigns"
      />
    </div>

    <!-- No Active Pregnancy State -->
    <div v-else class="text-center py-12">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No active pregnancy</h3>
      <p class="mt-1 text-sm text-gray-500">Start tracking your pregnancy journey today.</p>
      <div class="mt-6">
        <button
          @click="showCreateForm = true"
          class="btn btn-primary"
        >
          Start Pregnancy Tracking
        </button>
      </div>
    </div>

    <!-- Create Pregnancy Modal -->
    <PregnancyForm
      v-if="showCreateForm"
      @close="showCreateForm = false"
      @saved="handlePregnancySaved"
    />

    <!-- Create Appointment Modal -->
    <AppointmentForm
      v-if="showAppointmentForm"
      :pregnancy-id="pregnancyStore.activePregnancy?.id"
      @close="showAppointmentForm = false"
      @saved="handleAppointmentSaved"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePregnancyStore } from '../stores/pregnancy'
import { formatDate, calculatePregnancyWeeks } from '../utils/dates'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

// Import pregnancy components
import WeeklyInfoCard from '../components/pregnancy/WeeklyInfoCard.vue'
import AppointmentsCard from '../components/pregnancy/AppointmentsCard.vue'
import HealthTipsCard from '../components/pregnancy/HealthTipsCard.vue'
import DangerSignsCard from '../components/pregnancy/DangerSignsCard.vue'
import PregnancyForm from '../components/forms/PregnancyForm.vue'
import AppointmentForm from '../components/forms/AppointmentForm.vue'

export default {
  name: 'PregnancyTracker',
  components: {
    LoadingSpinner,
    WeeklyInfoCard,
    AppointmentsCard,
    HealthTipsCard,
    DangerSignsCard,
    PregnancyForm,
    AppointmentForm
  },
  setup() {
    const pregnancyStore = usePregnancyStore()
    const showCreateForm = ref(false)
    const showAppointmentForm = ref(false)

    const weeksRemaining = computed(() => {
      if (!pregnancyStore.activePregnancy?.due_date) return 0
      const { weeksRemaining } = calculatePregnancyWeeks(pregnancyStore.activePregnancy.due_date)
      return Math.max(0, weeksRemaining)
    })

    const progressPercentage = computed(() => {
      if (!pregnancyStore.currentWeek) return 0
      return Math.min(100, (pregnancyStore.currentWeek / 40) * 100)
    })

    const nextAppointmentDate = computed(() => {
      const appointments = pregnancyStore.upcomingAppointments
      if (appointments.length === 0) return null
      return formatDate(appointments[0].scheduled_date)
    })

    const handlePregnancySaved = () => {
      showCreateForm.value = false
      pregnancyStore.fetchPregnancies()
      pregnancyStore.fetchWeeklyInfo()
    }

    const handleAppointmentSaved = () => {
      showAppointmentForm.value = false
      pregnancyStore.fetchAppointments()
    }

    onMounted(async () => {
      await pregnancyStore.fetchPregnancies()
      if (pregnancyStore.activePregnancy) {
        await Promise.all([
          pregnancyStore.fetchWeeklyInfo(),
          pregnancyStore.fetchAppointments(),
          pregnancyStore.fetchDangerSigns()
        ])
      }
    })

    return {
      pregnancyStore,
      showCreateForm,
      showAppointmentForm,
      weeksRemaining,
      progressPercentage,
      nextAppointmentDate,
      handlePregnancySaved,
      handleAppointmentSaved,
      formatDate
    }
  }
}
</script>