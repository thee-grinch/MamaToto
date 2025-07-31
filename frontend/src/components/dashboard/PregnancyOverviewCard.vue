<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4">Pregnancy Overview</h2>
    <div class="space-y-3">
      <p><strong>Weeks Pregnant:</strong> {{ weeksPregnant }}</p>
      <p><strong>Due Date:</strong> {{ dueDate }}</p>
      <p><strong>Next Appointment:</strong> {{ nextAppointment }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  weeksPregnant: {
    type: String,
    default: 'N/A'
  },
  dueDate: {
    type: String,
    default: 'N/A'
  },
  nextAppointment: {
    type: String,
    default: 'N/A'
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed,
   but prefer using Tailwind classes in the template. */
</style>