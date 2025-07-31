<template>
  <div class="bg-white shadow rounded-lg p-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Upcoming Appointments</h3>
    
    <div v-if="upcomingAppointments && upcomingAppointments.length > 0">
      <ul class="list-disc list-inside space-y-2">
        <li v-for="appointment in upcomingAppointments" :key="appointment.id" class="text-sm text-gray-700">
          {{ appointment.scheduled_date }}: {{ appointment.description }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="text-sm text-gray-500">No upcoming appointments scheduled.</p>
    </div>

    </div>
</template>

<script>
import { computed } from 'vue';
import { usePregnancyStore } from '../../stores/pregnancy';

export default {
  name: 'AppointmentsCard',
  setup() {
    const pregnancyStore = usePregnancyStore();
    
    const upcomingAppointments = computed(() => pregnancyStore.upcomingAppointments);

    return {
      upcomingAppointments,
    };
  },
};
</script>