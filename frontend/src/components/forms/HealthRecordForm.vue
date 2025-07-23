
<!-- src/components/forms/HealthRecordForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-full max-w-lg shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ record ? 'Update Health Record' : 'Add Health Record' }}
          </h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="record_type" class="form-label">Type *</label>
              <select
                id="record_type"
                v-model="form.record_type"
                required
                class="form-input"
              >
                <option value="">Select type</option>
                <option value="symptom">Symptom</option>
                <option value="medication">Medication</option>
                <option value="test_result">Test Result</option>
                <option value="general">General Note</option>
              </select>
            </div>

            <div>
              <label for="recorded_date" class="form-label">Date *</label>
              <input
                id="recorded_date"
                v-model="form.recorded_date"
                type="date"
                required
                class="form-input"
              />
            </div>
          </div>

          <div>
            <label for="title" class="form-label">Title *</label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="form-input"
              placeholder="Brief description"
            />
          </div>

          <div>
            <label for="severity" class="form-label">Severity</label>
            <select
              id="severity"
              v-model="form.severity"
              class="form-input"
            >
              <option value="">Select severity</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <div>
            <label for="description" class="form-label">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="4"
              class="form-input"
              placeholder="Detailed description of the health record..."
            ></textarea>
          </div>

          <div>
            <label for="action_taken" class="form-label">Action Taken</label>
            <textarea
              id="action_taken"
              v-model="form.action_taken"
              rows="2"
              class="form-input"
              placeholder="What actions were taken..."
            ></textarea>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="btn btn-outline"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="btn btn-primary"
            >
              <LoadingSpinner v-if="loading" size="small" class="mr-2" />
              {{ record ? 'Update' : 'Save Record' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import { useHealthStore } from '../../stores/health'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'HealthRecordForm',
  components: {
    LoadingSpinner
  },
  props: {
    record: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const healthStore = useHealthStore()
    const loading = ref(false)

    const form = reactive({
      record_type: '',
      title: '',
      description: '',
      severity: '',
      recorded_date: new Date().toISOString().split('T')[0],
      action_taken: ''
    })

    const initializeForm = () => {
      if (props.record) {
        Object.keys(form).forEach(key => {
          if (props.record[key] !== undefined) {
            form[key] = props.record[key]
          }
        })
      }
    }

    const handleSubmit = async () => {
      loading.value = true

      const recordData = {
        record_type: form.record_type,
        title: form.title,
        description: form.description || null,
        severity: form.severity || null,
        recorded_date: form.recorded_date,
        action_taken: form.action_taken || null
      }

      const success = await healthStore.createHealthRecord(recordData)
      loading.value = false

      if (success) {
        emit('saved')
      }
    }

    onMounted(() => {
      initializeForm()
    })

    return {
      form,
      loading,
      handleSubmit
    }
  }
</script>