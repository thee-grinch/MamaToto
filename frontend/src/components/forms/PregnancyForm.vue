<!-- src/components/forms/PregnancyForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ pregnancy ? 'Update Pregnancy' : 'Start Pregnancy Tracking' }}
          </h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="due_date" class="form-label">Due Date *</label>
            <input
              id="due_date"
              v-model="form.due_date"
              type="date"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.due_date }"
            />
            <p v-if="errors.due_date" class="form-error">{{ errors.due_date }}</p>
          </div>

          <div>
            <label for="last_weight" class="form-label">Current Weight (kg)</label>
            <input
              id="last_weight"
              v-model.number="form.last_weight"
              type="number"
              step="0.1"
              min="30"
              max="200"
              class="form-input"
              placeholder="65.5"
            />
          </div>

          <div>
            <label for="last_checkup" class="form-label">Last Checkup Date</label>
            <input
              id="last_checkup"
              v-model="form.last_checkup"
              type="date"
              class="form-input"
            />
          </div>

          <div>
            <label for="complications" class="form-label">Complications or Notes</label>
            <textarea
              id="complications"
              v-model="form.complications"
              rows="3"
              class="form-input"
              placeholder="Any pregnancy complications or special notes..."
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
              {{ pregnancy ? 'Update' : 'Start Tracking' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import { usePregnancyStore } from '../../stores/pregnancy'
import { validateDate } from '../../utils/validation'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'PregnancyForm',
  components: {
    LoadingSpinner
  },
  props: {
    pregnancy: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const pregnancyStore = usePregnancyStore()
    const loading = ref(false)
    const errors = ref({})

    const form = reactive({
      due_date: '',
      last_weight: null,
      last_checkup: '',
      complications: ''
    })

    const initializeForm = () => {
      if (props.pregnancy) {
        form.due_date = props.pregnancy.due_date
        form.last_weight = props.pregnancy.last_weight
        form.last_checkup = props.pregnancy.last_checkup || ''
        form.complications = props.pregnancy.complications || ''
      }
    }

    const validateForm = () => {
      errors.value = {}

      if (!form.due_date) {
        errors.value.due_date = 'Due date is required'
        return false
      }

      if (!validateDate(form.due_date)) {
        errors.value.due_date = 'Please enter a valid date'
        return false
      }

      const dueDate = new Date(form.due_date)
      const today = new Date()
      const minDate = new Date()
      minDate.setMonth(minDate.getMonth() - 9) // 9 months ago
      const maxDate = new Date()
      maxDate.setMonth(maxDate.getMonth() + 9) // 9 months from now

      if (dueDate < minDate || dueDate > maxDate) {
        errors.value.due_date = 'Due date should be within reasonable pregnancy timeframe'
        return false
      }

      return true
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      loading.value = true

      const pregnancyData = {
        due_date: form.due_date,
        last_weight: form.last_weight,
        last_checkup: form.last_checkup || null,
        complications: form.complications || null
      }

      let success
      if (props.pregnancy) {
        success = await pregnancyStore.updatePregnancy(props.pregnancy.id, pregnancyData)
      } else {
        success = await pregnancyStore.createPregnancy(pregnancyData)
      }

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
      errors,
      loading,
      handleSubmit
    }
  }
}
</script>