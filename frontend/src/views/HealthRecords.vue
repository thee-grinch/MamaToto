<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Health Records</h1>
      <p class="mt-1 text-sm text-gray-500">View and manage your health records.</p>
    </div>

    <!-- Add Health Record Button -->
    <div class="flex justify-end">
      <button @click="showHealthRecordForm = true; editingRecord = null" class="btn btn-primary">
        Add Health Record
      </button>
    </div>

    <!-- Health Records List -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Your Records</h3>
        
        <div v-if="healthStore.healthRecords.length > 0" class="space-y-4">
          <div
            v-for="record in healthStore.healthRecords"
            :key="record.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-md font-medium text-gray-900">{{ record.title }}</h4>
              <span :class="[severityBadgeClass(record.severity)]">{{ record.severity }}</span>
            </div>
            <p class="text-sm text-gray-500">{{ record.record_type }} - {{ formatDate(record.recorded_date) }}</p>
            <p v-if="record.description" class="mt-2 text-sm text-gray-700">{{ record.description }}</p>
            <p v-if="record.action_taken" class="mt-2 text-sm text-gray-700 font-medium">Action Taken: {{ record.action_taken }}</p>

            <div class="mt-4 flex justify-end space-x-3">
              <button @click="startEditingRecord(record)" class="text-sm text-indigo-600 hover:text-indigo-900">
                Edit
              </button>
              <button @click="deleteRecord(record.id)" class="text-sm text-red-600 hover:text-red-900">
                Delete
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-4">
          <p class="text-sm text-gray-500">No health records found.</p>
        </div>
      </div>
    </div>

    <!-- Health Record Form Modal -->
    <HealthRecordForm
      v-if="showHealthRecordForm"
      :record="editingRecord"
      @close="showHealthRecordForm = false; editingRecord = null"
      @saved="handleRecordSaved"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useHealthStore } from '../stores/health'
import { formatDate } from '../utils/dates'
import HealthRecordForm from '../components/forms/HealthRecordForm.vue'

export default {
  name: 'HealthRecords',
  components: {
    HealthRecordForm
  },
  setup() {
    const healthStore = useHealthStore()
    const showHealthRecordForm = ref(false)
    const editingRecord = ref(null)

    const severityBadgeClass = (severity) => {
      switch (severity) {
        case 'low': return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
        case 'medium': return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800';
        case 'high': return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800';
        case 'critical': return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800';
        default: return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800';
      }
    }

    const startEditingRecord = (record) => {
      editingRecord.value = record;
      showHealthRecordForm.value = true;
    };

    const deleteRecord = async (recordId) => {
      if (confirm('Are you sure you want to delete this health record?')) {
        const success = await healthStore.deleteHealthRecord(recordId);
        if (success) {
          // Show success message
          console.log('Health record deleted successfully');
          healthStore.fetchHealthRecords(); // Refresh the list
        }
      }
    };

    const handleRecordSaved = () => {
      showHealthRecordForm.value = false;
      editingRecord.value = null;
      healthStore.fetchHealthRecords(); // Refresh the list
    };

    onMounted(() => {
      healthStore.fetchHealthRecords();
    });

    return {
      healthStore,
      showHealthRecordForm,
      editingRecord,
      severityBadgeClass,
      startEditingRecord,
      deleteRecord,
      handleRecordSaved,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>