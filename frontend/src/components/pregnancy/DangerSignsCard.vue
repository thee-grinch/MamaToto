<template>
  <div class="bg-white shadow rounded-lg p-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Danger Signs</h3>
    
    <div v-if="dangerSigns && dangerSigns.length > 0">
      <ul class="list-disc list-inside space-y-2">
        <li v-for="sign in dangerSigns" :key="sign.id" class="text-sm text-gray-700">
          {{ sign.description }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="text-sm text-gray-500">No danger signs recorded or relevant for this stage.</p>
    </div>

    </div>
</template>

<script>
import { computed } from 'vue';
import { usePregnancyStore } from '../../stores/pregnancy';

export default {
  name: 'DangerSignsCard',
  setup() {
    const pregnancyStore = usePregnancyStore();
    
    const dangerSigns = computed(() => pregnancyStore.dangerSigns);

    return {
      dangerSigns,
    };
  },
};
</script>