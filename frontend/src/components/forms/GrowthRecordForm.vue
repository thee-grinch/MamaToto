<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Add Growth Measurement
              </h3>
              <div class="mt-6 space-y-5">
                <div>
                  <label for="recorded_date" class="form-label">Date *</label>
                  <input type="date" name="recorded_date" id="recorded_date" v-model="form.recorded_date" required class="form-input" />
                </div>
                <div>
                  <label for="weight" class="form-label">Weight (kg) *</label>
                  <input type="number" name="weight" id="weight" v-model.number="form.weight" required class="form-input" step="0.01" />
                </div>
                <div>
                  <label for="height" class="form-label">Height (cm) *</label>
                  <input type="number" name="height" id="height" v-model.number="form.height" required class="form-input" step="0.1" />
                </div>
                 <div>
                  <label for="notes" class="form-label">Notes</label>
                  <textarea name="notes" id="notes" v-model="form.notes" rows="2" class="form-input" placeholder="Any specific observations..."></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-pink-600 text-base font-medium text-white hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 sm:ml-3 sm:w-auto sm:text-sm"
            @click="saveRecord"
            :disabled="loading"
          >
            {{ loading ? 'Saving...' : 'Save Measurement' }}
          </button>
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="closeForm"
            :disabled="loading"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { useChildrenStore } from '../../stores/children'; // Assuming the children store is in this path

const props = defineProps({
  childId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['close', 'saved']);

const childrenStore = useChildrenStore();
const loading = ref(false);

const form = reactive({
  recorded_date: '',
  weight: null,
  height: null,
  notes: '',
});

const saveRecord = async () => {
  // Basic validation
  if (!form.recorded_date || form.weight === null || form.height === null) {
    alert('Please fill in date, weight, and height.');
    return;
  }

  loading.value = true;
  try {
    // Assuming an action in childrenStore to add a growth record
    await childrenStore.addGrowthRecord(props.childId, {
      recorded_date: form.recorded_date,
      weight: form.weight,
      height: form.height,
      notes: form.notes || null,
    });
    emit('saved');
  } catch (error) {
    console.error('Error saving growth record:', error);
    alert('Failed to save growth record. Please try again.'); // Basic error display
  } finally {
    loading.value = false;
  }
};

const closeForm = () => {
  emit('close');
};
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>