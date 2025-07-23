<!-- src/components/forms/ChildForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ child ? 'Update Child' : 'Add Child' }}
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
            <label for="name" class="form-label">Child's Name *</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.name }"
              placeholder="Enter child's name"
            />
            <p v-if="errors.name" class="form-error">{{ errors.name }}</p>
          </div>

          <div>
            <label for="birth_date" class="form-label">Birth Date *</label>
            <input
              id="birth_date"
              v-model="form.birth_date"
              type="date"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.birth_date }"
            />
            <p v-if="errors.birth_date" class="form-error">{{ errors.birth_date }}</p>
          </div>

          <div>
            <label for="gender" class="form-label">Gender</label>
            <select
              id="gender"
              v-model="form.gender"
              class="form-input"
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="birth_weight" class="form-label">Birth Weight (kg)</label>
              <input
                id="birth_weight"
                v-model.number="form.birth_weight"
                type="number"
                step="0.01"
                min="0.5"
                max="10"
                class="form-input"
                placeholder="3.5"
              />
            </div>

            <div>
              <label for="birth_length" class="form-label">Birth Length (cm)</label>
              <input
                id="birth_length"
                v-model.number="form.birth_length"
                type="number"
                step="0.1"
                min="30"
                max="70"
                class="form-input"
                placeholder="50"
              />
            </div>
          </div>

          <div>
            <label for="birth_complications" class="form-label">Birth Complications</label>
            <textarea
              id="birth_complications"
              v-model="form.birth_complications"
              rows="3"
              class="form-input"
              placeholder="Any complications during birth or special notes..."
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
              {{ child ? 'Update' : 'Add Child' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import { useChildrenStore } from '../../stores/children'
import { validateDate } from '../../utils/validation'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'ChildForm',
  components: {
    LoadingSpinner
  },
  props: {
    child: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const childrenStore = useChildrenStore()
    const loading = ref(false)
    const errors = ref({})

    const form = reactive({
      name: '',
      birth_date: '',
      gender: '',
      birth_weight: null,
      birth_length: null,
      birth_complications: ''
    })

    const initializeForm = () => {
      if (props.child) {
        form.name = props.child.name
        form.birth_date = props.child.birth_date
        form.gender = props.child.gender || ''
        form.birth_weight = props.child.birth_weight
        form.birth_length = props.child.birth_length
        form.birth_complications = props.child.birth_complications || ''
      }
    }

    const validateForm = () => {
      errors.value = {}
      let isValid = true

      if (!form.name.trim()) {
        errors.value.name = 'Child\'s name is required'
        isValid = false
      }

      if (!form.birth_date) {
        errors.value.birth_date = 'Birth date is required'
        isValid = false
      } else if (!validateDate(form.birth_date)) {
        errors.value.birth_date = 'Please enter a valid date'
        isValid = false
      } else {
        const birthDate = new Date(form.birth_date)
        const today = new Date()
        const maxAge = new Date()
        maxAge.setFullYear(maxAge.getFullYear() - 18) // Max 18 years old

        if (birthDate > today) {
          errors.value.birth_date = 'Birth date cannot be in the future'
          isValid = false
        } else if (birthDate < maxAge) {
          errors.value.birth_date = 'Child must be under 18 years old'
          isValid = false
        }
      }

      return isValid
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      loading.value = true

      const childData = {
        name: form.name.trim(),
        birth_date: form.birth_date,
        gender: form.gender || null,
        birth_weight: form.birth_weight,
        birth_length: form.birth_length,
        birth_complications: form.birth_complications || null
      }

      let success
      if (props.child) {
        success = await childrenStore.updateChild(props.child.id, childData)
      } else {
        success = await childrenStore.createChild(childData)
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