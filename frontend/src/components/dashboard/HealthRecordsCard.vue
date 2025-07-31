<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold mb-4">Recent Health Records</h3>
    <div v-if="records && records.length > 0">
      <ul class="space-y-3">
        <li v-for="record in records" :key="record.id" class="flex items-center justify-between">
          <span>{{ record.type }} - {{ record.date }}</span>
          <!-- Add other relevant health record info here if available -->
          <!-- For example: <span>{{ record.value }} {{ record.unit }}</span> -->
        </li>
      </ul>
    </div>
    <div v-else class="text-gray-500">No recent health records found.</div>
    <!-- Optional: Add a link to view all health records -->
    <!-- <div class="mt-4 text-right">
      <router-link to="/health-records" class="text-blue-600 hover:underline">View All Records</router-link>
    </div> -->
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  records: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>