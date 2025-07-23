<!-- src/components/child/VaccinationTracker.vue -->
<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-lg font-medium text-gray-900">Vaccination Schedule</h4>
      <button
        @click="showAddVaccinationForm = true"
        class="btn btn-sm btn-primary"
      >
        Record Vaccination
      </button>
    </div>

    <LoadingSpinner v-if="childrenStore.loading" size="medium" />

    <div v-else-if="vaccinations.length > 0" class="space-y-3">
      <div
        v-for="vaccination in vaccinations"
        :key="vaccination.id"
        class="flex items-center justify-between p-4 border rounded-lg"
        :class="getVaccinationStatusColor(vaccination.status)"
      >
        <div class="flex-1">
          <h5 class="font-medium text-gray-900">{{ vaccination.vaccine_name }}</h5>
          <p class="text-sm text-gray-600">{{ vaccination.description || 'No description' }}</p>
          <div class="flex items-center space-x-4 mt-1 text-sm">
            <span class="text-gray-500">Due: {{ formatDate(vaccination.scheduled_date) }}</span>
            <span v-if="vaccination.administered_date" class="text-green-600">
              Given: {{ formatDate(vaccination.administered_date) }}
            </span>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <span :class="getStatusBadgeClass(vaccination.status)" class="badge">
            {{ vaccination.status }}
          </span>
          <button
            v-if="vaccination.status === 'pending'"
            @click="markAsGiven(vaccination)"
            class="btn btn-sm btn-success"
          >
            Mark as Given
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No vaccinations scheduled</h3>
      <p class="mt-1 text-sm text-gray-500">Vaccination schedule will be created automatically.</p>
    </div>

    <!-- Add Vaccination Form Modal -->
    <VaccinationForm
      v-if="showAddVaccinationForm"
      :child-id="childId"
      @close="showAddVaccinationForm = false"
      @saved="handleVaccinationSaved"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useChildrenStore } from '../../stores/children'
import { formatDate } from '../../utils/dates'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import VaccinationForm from '../forms/VaccinationForm.vue'

export default {
  name: 'VaccinationTracker',
  components: {
    LoadingSpinner,
    VaccinationForm
  },
  props: {
    childId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const childrenStore = useChildrenStore()
    const showAddVaccinationForm = ref(false)

    const vaccinations = computed(() => {
      return childrenStore.getChildVaccinations(props.childId)
    })

    const getVaccinationStatusColor = (status) => {
      const colors = {
        completed: 'border-green-200 bg-green-50',
        pending: 'border-yellow-200 bg-yellow-50',
        overdue: 'border-red-200 bg-red-50',
        skipped: 'border-gray-200 bg-gray-50'
      }
      return colors[status] || 'border-gray-200 bg-white'
    }

    const getStatusBadgeClass = (status) => {
      const classes = {
        completed: 'badge-success',
        pending: 'badge-warning',
        overdue: 'badge-danger',
        skipped: 'badge-gray'
      }
      return classes[status] || 'badge-gray'
    }

    const markAsGiven = async (vaccination) => {
      // TODO: Implement mark as given functionality
      console.log('Mark vaccination as given:', vaccination)
    }

    const handleVaccinationSaved = () => {
      showAddVaccinationForm.value = false
      childrenStore.fetchChildVaccinations(props.childId)
    }

    onMounted(() => {
      childrenStore.fetchChildVaccinations(props.childId)
    })

    return {
      childrenStore,
      showAddVaccinationForm,
      vaccinations,
      getVaccinationStatusColor,
      getStatusBadgeClass,
      markAsGiven,
      handleVaccinationSaved,
      formatDate
    }
  }
}
</script>