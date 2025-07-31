<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold mb-4">Upcoming Appointments</h3>
    <div v-if="appointments && appointments.length > 0">
      <ul class="space-y-3">
        <li v-for="appointment in appointments" :key="appointment.id" class="text-sm text-gray-700">
          {{ appointment.date }} - {{ appointment.time }} - {{ appointment.location }}
          <!-- Add other relevant appointment info here if available -->
          <!-- For example: <span>{{ appointment.notes }}</span> -->
        </li>
      </ul>
    </div>
    <div v-else class="text-gray-500">No upcoming appointments.</div>
    <!-- Optional: Add a link to add a new appointment or view all appointments -->
    <!-- <div class="mt-4 text-right">
      <router-link to="/appointments" class="text-blue-600 hover:underline">View All Appointments</router-link>
    </div> -->
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  appointments: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>