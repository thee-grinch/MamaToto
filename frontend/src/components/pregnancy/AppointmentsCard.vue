<template>
  <div class="bg-white shadow rounded-lg p-4 sm:p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Upcoming Appointments</h3>
      <!-- Optional: Add button to add new appointment -->
      <!-- <button class="btn btn-sm btn-outline">Add Appointment</button> -->
    </div>
    
    <div v-if="appointments.length > 0" class="space-y-3">
      <div
        v-for="appointment in appointments"
        :key="appointment.id"
        class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
      >
        <div>
          <p class="font-medium text-gray-900">{{ appointment.title || 'Appointment' }}</p>
          <p class="text-sm text-gray-600">{{ formatDate(appointment.scheduled_date) }}</p>
          <p v-if="appointment.location" class="text-sm text-gray-500">{{ appointment.location }}</p>
        </div>
        <!-- Optional: Add actions like edit/delete appointment -->
        <!-- <div class="flex items-center space-x-2">
          <button class="text-gray-400 hover:text-gray-600">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
          </button>
          <button class="text-gray-400 hover:text-gray-600">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
          </button>
        </div> -->
      </div>
    </div>
    
    <div v-else class="text-center py-4">
      <p class="text-sm text-gray-500">No upcoming appointments.</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { usePregnancyStore } from '../../stores/pregnancy';
import { formatDate } from '../../utils/dates';

export default {
  name: 'AppointmentsCard',
  setup() {
    const pregnancyStore = usePregnancyStore();

    const appointments = computed(() => pregnancyStore.upcomingAppointments);

    return {
      appointments,
      formatDate,
    };
  },
};
</script>