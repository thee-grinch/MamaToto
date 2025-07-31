<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                {{ appointment ? 'Edit Appointment' : 'Add New Appointment' }}
              </h3>
              <div class="mt-6 space-y-5">
                <div>
                  <label for="scheduled_date" class="form-label">Date *</label>
                  <input type="date" name="scheduled_date" id="scheduled_date" v-model="form.scheduled_date" required class="form-input" />
                </div>
                <div>
                  <label for="scheduled_time" class="form-label">Time</label>
                  <input type="time" name="scheduled_time" id="scheduled_time" v-model="form.scheduled_time" class="form-input" />
                </div>
                <div>
                  <label for="location" class="form-label">Location</label>
                  <input type="text" name="location" id="location" v-model="form.location" class="form-input" placeholder="e.g., Clinic Name" />
                </div>
                <div>
                  <label for="notes" class="form-label">Notes</label>
                  <textarea name="notes" id="notes" v-model="form.notes" rows="3" class="form-input" placeholder="Any specific instructions or questions..."></textarea>
                </div>
                <div class="flex items-center">
                    <input id="completed" name="completed" type="checkbox" v-model="form.completed" class="form-checkbox h-4 w-4 text-pink-600 transition duration-150 ease-in-out" />
                    <label for="completed" class="ml-2 block text-sm leading-5 text-gray-900">Mark as Completed</label>
                  </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-pink-600 text-base font-medium text-white hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 sm:ml-3 sm:w-auto sm:text-sm"
            @click="saveAppointment"
          >
            {{ appointment ? 'Update Appointment' : 'Save Appointment' }}
          </button>
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="closeForm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, watch } from 'vue';
import { usePregnancyStore } from '../stores/pregnancy';

export default {
  name: 'AppointmentForm',
  props: {
    appointment: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const pregnancyStore = usePregnancyStore();
    const form = reactive({
      scheduled_date: '',
      scheduled_time: '',
      location: '',
      notes: '',
      completed: false,
    });

    const initializeForm = () => {
      if (props.appointment) {
        Object.keys(form).forEach(key => {
           if (props.appointment[key] !== undefined) {
            form[key] = props.appointment[key];
           }
        });
      }
    };

    const saveAppointment = async () => {
      // Basic validation
      if (!form.scheduled_date) {
        alert('Please select a date for the appointment.');
        return;
      }

      let success;
      if (props.appointment) {
        success = await pregnancyStore.updateAppointment(props.appointment.id, {
           scheduled_date: form.scheduled_date,
           scheduled_time: form.scheduled_time || null,
           location: form.location || null,
           notes: form.notes || null,
           completed: form.completed,
        });
      } else {
        // Assuming activePregnancy ID is needed for creation
        if (!pregnancyStore.activePregnancy) {
            alert('No active pregnancy to add appointment to.');
            return;
        }
        success = await pregnancyStore.createAppointment({
          pregnancy_id: pregnancyStore.activePregnancy.id,
          scheduled_date: form.scheduled_date,
          scheduled_time: form.scheduled_time || null,
          location: form.location || null,
          notes: form.notes || null,
          completed: form.completed,
        });
      }

      if (success) {
        emit('saved');
      }
    };

    const closeForm = () => {
      emit('close');
    };

    // Initialize form when the appointment prop changes (for editing)
    watch(() => props.appointment, (newAppointment) => {
      if (newAppointment) {
        initializeForm();
      }
    }, { immediate: true }); // Initialize immediately if appointment prop is already set on mount

    return {
      form,
      saveAppointment,
      closeForm,
    };
  },
};
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>