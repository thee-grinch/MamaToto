<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold mb-4">Alerts and Notifications</h3>

    <div v-if="(overdueVaccinations && overdueVaccinations.length > 0) || (growthAlerts && growthAlerts.length > 0)">
      <!-- Overdue Vaccinations -->
      <div v-if="overdueVaccinations && overdueVaccinations.length > 0" class="mb-4">
        <h4 class="text-md font-medium text-red-600 mb-2">Overdue Vaccinations</h4>
        <ul class="space-y-2">
          <li v-for="vaccination in overdueVaccinations" :key="vaccination.id" class="text-sm text-gray-700">
            {{ vaccination.childName }} - {{ vaccination.vaccineName }} (Due: {{ vaccination.dueDate }})
          </li>
        </ul>
      </div>

      <!-- Growth Alerts -->
      <div v-if="growthAlerts && growthAlerts.length > 0">
        <h4 class="text-md font-medium text-yellow-600 mb-2">Growth Alerts</h4>
        <ul class="space-y-2">
          <li v-for="alert in growthAlerts" :key="alert.id" class="text-sm text-gray-700">
            {{ alert.childName }} - {{ alert.message }} (Date: {{ alert.date }})
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="text-gray-500">No new alerts.</div>

    <!-- Optional: Add a link to view all alerts -->
    <!-- <div class="mt-4 text-right">
      <router-link to="/alerts" class="text-blue-600 hover:underline">View All Alerts</router-link>
    </div> -->
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  overdueVaccinations: {
    type: Array,
    default: () => []
  },
  growthAlerts: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>