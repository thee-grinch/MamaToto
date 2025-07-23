<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Health Records</h1>
        <p class="mt-1 text-sm text-gray-500">Track symptoms, medications, and health notes</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button
          @click="showAddRecordForm = true"
          class="btn btn-primary"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Health Record
        </button>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          v-for="filter in filters"
          :key="filter.key"
          @click="activeFilter = filter.key"
          :class="[
            activeFilter === filter.key
              ? 'border-pink-500 text-pink-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
          ]"
        >
          {{ filter.label }}
          <span v-if="filter.count > 0" 
                :class="[
                  activeFilter === filter.key ? 'bg-pink-100 text-pink-600' : 'bg-gray-100 text-gray-900',
                  'ml-2 inline-block py-0.5 px-2 text-xs rounded-full'
                ]">
            {{ filter.count }}
          </span>
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <LoadingSpinner v-if="healthStore.loading" size="large" message="Loading health records..." />

    <!-- Health Records List -->
    <div v-else-if="filteredRecords.length > 0" class="space-y-4">
      <HealthRecordCard
        v-for="record in filteredRecords"
        :key="record.id"
        :record="record"
        @edit="editRecord"
        @delete="deleteRecord"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No health records</h3>
      <p class="mt-1 text-sm text-gray-500">
        {{ activeFilter === 'all' ? 'Start tracking your health journey.' : `No ${activeFilter} records found.` }}
      </p>
      <div class="mt-6">
        <button
          @click="showAddRecordForm = true"
          class="btn btn-primary"
        >
          Add Your First Record
        </button>
      </div>
    </div>

    <!-- Mental Health Assessment Button -->
    <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-sm font-medium text-purple-900">Mental Health Check</h3>
          <p class="text-sm text-purple-700">Take a quick assessment to monitor your mental wellbeing</p>
        </div>
        <button
          @click="showMentalHealthForm = true"
          class="btn btn-secondary bg-purple-100 text-purple-700 hover:bg-purple-200"
        >
          Take Assessment
        </button>
      </div>
    </div>

    <!-- Add Health Record Modal -->
    <HealthRecordForm
      v-if="showAddRecordForm"
      @close="showAddRecordForm = false"
      @saved="handleRecordSaved"
    />

    <!-- Edit Health Record Modal -->
    <HealthRecordForm
      v-if="showEditRecordForm && editingRecord"
      :record="editingRecord"
      @close="showEditRecordForm = false"
      @saved="handleRecordSaved"
    />

    <!-- Mental Health Assessment Modal -->
    <MentalHealthForm
      v-if="showMentalHealthForm"
      @close="showMentalHealthForm = false"
      @saved="handleAssessmentSaved"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '../stores/health'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

// Import health components
import HealthRecordCard from '../components/health/HealthRecordCard.vue'
import HealthRecordForm from '../components/forms/HealthRecordForm.vue'
import MentalHealthForm from '../components/forms/MentalHealthForm.vue'

export default {
  name: 'HealthRecords',
  components: {
    LoadingSpinner,
    HealthRecordCard,
    HealthRecordForm,
    MentalHealthForm
  },
  setup() {
    const healthStore = useHealthStore()
    const activeFilter = ref('all')
    const showAddRecordForm = ref(false)
    const showEditRecordForm = ref(false)
    const showMentalHealthForm = ref(false)
    const editingRecord = ref(null)

    const filters = computed(() => [
      {
        key: 'all',
        label: 'All Records',
        count: healthStore.healthRecords.length
      },
      {
        key: 'symptom',
        label: 'Symptoms',
        count: healthStore.healthRecords.filter(r => r.record_type === 'symptom').length
      },
      {
        key: 'medication',
        label: 'Medications',
        count: healthStore.healthRecords.filter(r => r.record_type === 'medication').length
      },
      {
        key: 'test_result',
        label: 'Test Results',
        count: healthStore.healthRecords.filter(r => r.record_type === 'test_result').length
      }
    ])

    const filteredRecords = computed(() => {
      if (activeFilter.value === 'all') {
        return healthStore.healthRecords
      }
      return healthStore.healthRecords.filter(record => 
        record.record_type === activeFilter.value
      )
    })

    const editRecord = (record) => {
      editingRecord.value = record
      showEditRecordForm.value = true
    }

    const deleteRecord = async (record) => {
      if (confirm('Are you sure you want to delete this health record?')) {
        // TODO: Implement delete functionality
        console.log('Delete record:', record)
      }
    }

    const handleRecordSaved = () => {
      showAddRecordForm.value = false
      showEditRecordForm.value = false
      editingRecord.value = null
      healthStore.fetchHealthRecords()
    }

    const handleAssessmentSaved = () => {
      showMentalHealthForm.value = false
      healthStore.fetchMentalHealthAssessments()
    }

    onMounted(() => {
      healthStore.fetchHealthRecords()
    })

    return {
      healthStore,
      activeFilter,
      showAddRecordForm,
      showEditRecordForm,
      showMentalHealthForm,
      editingRecord,
      filters,
      filteredRecords,
      editRecord,
      deleteRecord,
      handleRecordSaved,
      handleAssessmentSaved
    }
  }
}
</script>