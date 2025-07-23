<!-- src/components/child/ChildCard.vue -->
<template>
  <div class="bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer" @click="$emit('select', child)">
    <div class="p-6">
      <div class="flex items-center space-x-4">
        <div class="bg-blue-100 rounded-full p-3">
          <svg class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-gray-900">{{ child.name }}</h3>
          <p class="text-sm text-gray-500">{{ calculateAge(child.birth_date) }}</p>
          <p class="text-xs text-gray-400">Born {{ formatDate(child.birth_date) }}</p>
        </div>
        <div class="flex-shrink-0">
          <button
            @click.stop="$emit('edit', child)"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Quick Stats -->
      <div class="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div>
          <p class="text-gray-500">Vaccinations</p>
          <p class="font-medium text-green-600">Up to date</p>
        </div>
        <div>
          <p class="text-gray-500">Last checkup</p>
          <p class="font-medium text-gray-900">2 weeks ago</p>
        </div>
      </div>
      
      <!-- Age Badge -->
      <div class="mt-3 flex justify-between items-center">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {{ child.gender || 'Unknown' }}
        </span>
        <span class="text-xs text-gray-500">{{ child.age_months }} months old</span>
      </div>
    </div>
  </div>
</template>

<script>
import { calculateAge, formatDate } from '../../utils/dates'

export default {
  name: 'ChildCard',
  props: {
    child: {
      type: Object,
      required: true
    }
  },
  emits: ['select', 'edit'],
  setup() {
    return {
      calculateAge,
      formatDate
    }
  }
}
</script>