<!-- src/components/forms/VaccinationForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Record Vaccination</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="vaccine_name" class="form-label">Vaccine Name *</label>
            <select
              id="vaccine_name"
              v-model="form.vaccine_name"
              required
              class="form-input"
            >
              <option value="">Select vaccine</option>
              <option v-for="vaccine in commonVaccines" :key="vaccine.code" :value="vaccine.name">
                {{ vaccine.name }}
              </option>
            </select>
          </div>

          <div>
            <label for="scheduled_date" class="form-label">Scheduled Date *</label>
            <input
              id="scheduled_date"
              v-model="form.scheduled_date"
              type="date"
              required
              class="form-input"
            />
          </div>

          <div>
            <label for="administered_date" class="form-label">Date Given</label>
            <input
              id="administered_date"
              v-model="form.administered_date"
              type="date"
              class="form-input"
            />
          </div>

          <div>
            <label for="healthcare_provider" class="form-label">Healthcare Provider</label>
            <input
              id="healthcare_provider"
              v-model="form.healthcare_provider"
              type="text"
              class="form-input"
              placeholder="Hospital or clinic name"
            />
          </div>

          <div>
            <label for="batch_number" class="form-label">Batch Number</label>
            <input
              id="batch_number"
              v-model="form.batch_number"
              type="text"
              class="form-input"
              placeholder="Vaccine batch number"
            />
          </div>

          <div>
            <label for="notes" class="form-label">Notes</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="3"
              class="form-input"
              placeholder="Any reactions or notes..."
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
              Record Vaccination
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useChildrenStore } from '../../stores/children'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'VaccinationForm',
  components: {
    LoadingSpinner
  },
  props: {
    childId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const childrenStore = useChildrenStore()
    const loading = ref(false)

    const form = reactive({
      vaccine_name: '',
      scheduled_date: '',
      administered_date: '',
      healthcare_provider: '',
      batch_number: '',
      notes: ''
    })

    const commonVaccines = [
      { code: 'BCG', name: 'BCG (Tuberculosis)' },
      { code: 'OPV0', name: 'OPV 0 (Polio - Birth)' },
      { code: 'OPV1', name: 'OPV 1 (Polio - 1st dose)' },
      { code: 'OPV2', name: 'OPV 2 (Polio - 2nd dose)' },
      { code: 'OPV3', name: 'OPV 3 (Polio - 3rd dose)' },
      { code: 'PENTA1', name: 'DPT-HepB-Hib 1' },
      { code: 'PENTA2', name: 'DPT-HepB-Hib 2' },
      { code: 'PENTA3', name: 'DPT-HepB-Hib 3' },
      { code: 'PCV1', name: 'PCV 1 (Pneumococcal)' },
      { code: 'PCV2', name: 'PCV 2 (Pneumococcal)' },
      { code: 'PCV3', name: 'PCV 3 (Pneumococcal)' },
      { code: 'ROTA1', name: 'Rotavirus 1' },
      { code: 'ROTA2', name: 'Rotavirus 2' },
      { code: 'IPV', name: 'IPV (Inactivated Polio)' },
      { code: 'MR1', name: 'Measles-Rubella 1' },
      { code: 'MR2', name: 'Measles-Rubella 2' },
      { code: 'YF', name: 'Yellow Fever' },
      { code: 'DPT_BOOSTER', name: 'DPT Booster' }
    ]

    const handleSubmit = async () => {
      loading.value = true

      const vaccinationData = {
        child_id: props.childId,
        vaccine_name: form.vaccine_name,
        scheduled_date: form.scheduled_date,
        administered_date: form.administered_date || null,
        healthcare_provider: form.healthcare_provider || null,
        batch_number: form.batch_number || null,
        notes: form.notes || null
      }

      const success = await childrenStore.createVaccination(props.childId, vaccinationData)
      loading.value = false

      if (success) {
        emit('saved')
      }
    }

    return {
      form,
      loading,
      commonVaccines,
      handleSubmit
    }
  }
}
</script>

<!-- src/components/forms/GrowthRecordForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Add Growth Measurement</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="recorded_date" class="form-label">Measurement Date *</label>
            <input
              id="recorded_date"
              v-model="form.recorded_date"
              type="date"
              required
              class="form-input"
            />
          </div>

          <div>
            <label for="weight" class="form-label">Weight (kg)</label>
            <input
              id="weight"
              v-model.number="form.weight"
              type="number"
              step="0.01"
              min="0.5"
              max="50"
              class="form-input"
              placeholder="e.g., 8.5"
            />
          </div>

          <div>
            <label for="height" class="form-label">Height (cm)</label>
            <input
              id="height"
              v-model.number="form.height"
              type="number"
              step="0.1"
              min="30"
              max="150"
              class="form-input"
              placeholder="e.g., 75.5"
            />
          </div>

          <div>
            <label for="head_circumference" class="form-label">Head Circumference (cm)</label>
            <input
              id="head_circumference"
              v-model.number="form.head_circumference"
              type="number"
              step="0.1"
              min="25"
              max="60"
              class="form-input"
              placeholder="e.g., 45.2"
            />
          </div>

          <div>
            <label for="notes" class="form-label">Notes</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="3"
              class="form-input"
              placeholder="Any observations or notes..."
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
              Save Measurement
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useChildrenStore } from '../../stores/children'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'GrowthRecordForm',
  components: {
    LoadingSpinner
  },
  props: {
    childId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const childrenStore = useChildrenStore()
    const loading = ref(false)

    const form = reactive({
      recorded_date: new Date().toISOString().split('T')[0],
      weight: null,
      height: null,
      head_circumference: null,
      notes: ''
    })

    const handleSubmit = async () => {
      loading.value = true

      const growthData = {
        child_id: props.childId,
        recorded_date: form.recorded_date,
        weight: form.weight,
        height: form.height,
        head_circumference: form.head_circumference,
        notes: form.notes || null
      }

      const success = await childrenStore.createGrowthRecord(props.childId, growthData)
      loading.value = false

      if (success) {
        emit('saved')
      }
    }

    return {
      form,
      loading,
      handleSubmit
    }
  }
}
</script>

<!-- src/components/forms/MilestoneForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Record Milestone</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="milestone_type" class="form-label">Category *</label>
            <select
              id="milestone_type"
              v-model="form.milestone_type"
              required
              class="form-input"
            >
              <option value="">Select category</option>
              <option value="motor">Motor Skills</option>
              <option value="language">Language</option>
              <option value="social">Social</option>
              <option value="cognitive">Cognitive</option>
            </select>
          </div>

          <div>
            <label for="milestone_name" class="form-label">Milestone *</label>
            <input
              id="milestone_name"
              v-model="form.milestone_name"
              type="text"
              required
              class="form-input"
              placeholder="e.g., First steps, Says first word"
            />
          </div>

          <div>
            <label for="typical_age_months" class="form-label">Typical Age (months)</label>
            <input
              id="typical_age_months"
              v-model.number="form.typical_age_months"
              type="number"
              min="0"
              max="60"
              class="form-input"
              placeholder="12"
            />
          </div>

          <div>
            <label for="achieved_date" class="form-label">Date Achieved</label>
            <input
              id="achieved_date"
              v-model="form.achieved_date"
              type="date"
              class="form-input"
            />
          </div>

          <div class="flex items-center">
            <input
              id="is_achieved"
              v-model="form.is_achieved"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="is_achieved" class="ml-2 block text-sm text-gray-900">
              Mark as achieved
            </label>
          </div>

          <div>
            <label for="notes" class="form-label">Notes</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="3"
              class="form-input"
              placeholder="Additional observations or context..."
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
              Save Milestone
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'MilestoneForm',
  components: {
    LoadingSpinner
  },
  props: {
    childId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const loading = ref(false)

    const form = reactive({
      milestone_type: '',
      milestone_name: '',
      typical_age_months: null,
      achieved_date: '',
      is_achieved: false,
      notes: ''
    })

    const handleSubmit = async () => {
      loading.value = true

      // TODO: Implement milestone creation API call
      console.log('Create milestone:', { ...form, child_id: props.childId })

      // Simulate API call
      setTimeout(() => {
        loading.value = false
        emit('saved')
      }, 1000)
    }

    return {
      form,
      loading,
      handleSubmit
    }
  }
}
</script>

<!-- src/components/forms/AppointmentForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Schedule Appointment</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="appointment_type" class="form-label">Appointment Type *</label>
            <select
              id="appointment_type"
              v-model="form.appointment_type"
              required
              class="form-input"
            >
              <option value="">Select type</option>
              <option value="anc">Antenatal Care</option>
              <option value="ultrasound">Ultrasound</option>
              <option value="specialist">Specialist Consultation</option>
              <option value="lab">Laboratory Test</option>
              <option value="checkup">General Checkup</option>
            </select>
          </div>

          <div>
            <label for="scheduled_date" class="form-label">Date *</label>
            <input
              id="scheduled_date"
              v-model="form.scheduled_date"
              type="date"
              required
              class="form-input"
            />
          </div>

          <div>
            <label for="location" class="form-label">Location</label>
            <input
              id="location"
              v-model="form.location"
              type="text"
              class="form-input"
              placeholder="Hospital or clinic name"
            />
          </div>

          <div>
            <label for="notes" class="form-label">Notes</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="3"
              class="form-input"
              placeholder="Additional details or reminders..."
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
              Schedule Appointment
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { usePregnancyStore } from '../../stores/pregnancy'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'AppointmentForm',
  components: {
    LoadingSpinner
  },
  props: {
    pregnancyId: {
      type: Number,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const pregnancyStore = usePregnancyStore()
    const loading = ref(false)

    const form = reactive({
      appointment_type: '',
      scheduled_date: '',
      location: '',
      notes: ''
    })

    const handleSubmit = async () => {
      loading.value = true

      const appointmentData = {
        pregnancy_id: props.pregnancyId,
        appointment_type: form.appointment_type,
        scheduled_date: form.scheduled_date,
        location: form.location || null,
        notes: form.notes || null
      }

      const success = await pregnancyStore.createAppointment(appointmentData)
      loading.value = false

      if (success) {
        emit('saved')
      }
    }

    return {
      form,
      loading,
      handleSubmit
    }
  }
}
</script>

<!-- src/components/forms/ChangePasswordForm.vue -->
<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Change Password</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="current_password" class="form-label">Current Password *</label>
            <input
              id="current_password"
              v-model="form.current_password"
              type="password"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.current_password }"
            />
            <p v-if="errors.current_password" class="form-error">{{ errors.current_password }}</p>
          </div>

          <div>
            <label for="new_password" class="form-label">New Password *</label>
            <input
              id="new_password"
              v-model="form.new_password"
              type="password"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.new_password }"
            />
            <p v-if="errors.new_password" class="form-error">{{ errors.new_password }}</p>
          </div>

          <div>
            <label for="confirm_password" class="form-label">Confirm New Password *</label>
            <input
              id="confirm_password"
              v-model="form.confirm_password"
              type="password"
              required
              class="form-input"
              :class="{ 'form-input-error': errors.confirm_password }"
            />
            <p v-if="errors.confirm_password" class="form-error">{{ errors.confirm_password }}</p>
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
              Change Password
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { validatePassword } from '../../utils/validation'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export default {
  name: 'ChangePasswordForm',
  components: {
    LoadingSpinner
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const loading = ref(false)
    const errors = ref({})

    const form = reactive({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })

    const validateForm = () => {
      errors.value = {}
      let isValid = true

      if (!validatePassword(form.new_password)) {
        errors.value.new_password = 'Password must be at least 6 characters'
        isValid = false
      }

      if (form.new_password !== form.confirm_password) {
        errors.value.confirm_password = 'Passwords do not match'
        isValid = false
      }

      return isValid
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      loading.value = true

      try {
        // TODO: Implement password change API call
        console.log('Change password:', {
          current_password: form.current_password,
          new_password: form.new_password
        })

        // Simulate API call
        setTimeout(() => {
          loading.value = false
          emit('saved')
        }, 1000)

      } catch (error) {
        loading.value = false
        errors.value.current_password = 'Current password is incorrect'
      }
    }

    return {
      form,
      errors,
      loading,
      handleSubmit
    }
  }
}
</script>