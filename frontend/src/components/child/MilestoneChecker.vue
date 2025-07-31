<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold mb-4">Developmental Milestones</h3>

    <div v-if="loading" class="text-center text-gray-500">Loading milestones...</div>
    <div v-else-if="error" class="text-center text-red-500">Error loading milestones: {{ error }}</div>
    <div v-else>
      <ul v-if="milestones.length" class="space-y-3">
        <li v-for="milestone in milestones" :key="milestone.id" class="flex items-center justify-between">
          <span>{{ milestone.description }}</span>
          <input type="checkbox" :checked="milestone.isAchieved" class="form-checkbox h-5 w-5 text-blue-600">
        </li>
      </ul>
      <div v-else class="text-gray-500">No milestones found for this child.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useChildStore } from '@/stores/child'; // Hypothetical child store

const props = defineProps({
  childId: {
    type: [String, Number],
    required: true
  }
});

const childStore = useChildStore();
const milestones = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchMilestones = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    // Assuming a store action to fetch milestones for a specific child
    await childStore.fetchChildMilestones(id);
    // Assuming the fetched milestones are stored in the childStore
    milestones.value = childStore.getChildMilestones(id) || [];
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchMilestones(props.childId);
});

watch(() => props.childId, (newChildId) => {
  if (newChildId) {
    fetchMilestones(newChildId);
  } else {
    milestones.value = [];
  }
});
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>