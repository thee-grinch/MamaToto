<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold mb-4">Children Overview</h3>
    <div v-if="children && children.length > 0">
      <ul class="space-y-3">
        <li v-for="child in children" :key="child.id" class="flex items-center justify-between">
          <span>{{ child.name }}</span>
          <!-- Add other relevant child info here if available in the child object -->
          <!-- For example: <span>Age: {{ child.age }}</span> -->
        </li>
      </ul>
    </div>
    <div v-else class="text-gray-500">No children added yet.</div>
    <!-- Optional: Add a link to manage children -->
    <!-- <div class="mt-4 text-right">
      <router-link to="/children" class="text-blue-600 hover:underline">Manage Children</router-link>
    </div> -->
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  children: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>