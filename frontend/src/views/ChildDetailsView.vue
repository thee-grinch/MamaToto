<template>
  <div class="container mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-6">Child Details</h1>
    <div v-if="loading" class="text-center text-gray-500">Loading child details...</div>
    <div v-else-if="error" class="text-center text-red-500">Error loading child details: {{ error }}</div>
    <div v-else-if="child">
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ child.name }}</h2>
        <p>Date of Birth: {{ child.dateOfBirth }}</p>
        <!-- Other child details -->
      </div>
      
      <!-- Milestone Checker Component -->
      <MilestoneChecker :childId="child.id" />
    </div>
    <div v-else class="text-center text-gray-500">Child not found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useChildStore } from '@/stores/child'; // Hypothetical child store
import MilestoneChecker from '@/components/child/MilestoneChecker.vue';
import { useRoute } from 'vue-router'; // Assuming you are using Vue Router

const route = useRoute();
const childStore = useChildStore();
const child = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const childId = route.params.id; // Assuming the child ID is passed as a route parameter
  if (childId) {
    try {
      await childStore.fetchChildDetails(childId); // Hypothetical store action
      child.value = childStore.getChildDetails(childId);
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }
});
</script>

<style scoped>
/* View-specific styles */
</style>
