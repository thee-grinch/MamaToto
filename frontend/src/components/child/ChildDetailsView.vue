<!-- src/components/child/ChildDetailsView.vue -->
<template>
  <div class="bg-white rounded-lg shadow">
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{{ child.name }} - Details</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <div class="p-6">
      <!-- Tabs -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              activeTab === tab.key
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <!-- Basic Info Tab -->
      <div v-if="activeTab === 'info'" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="text-sm font-medium text-gray-500 mb-2">Basic Information</h4>
            <dl class="space-y-2">
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Full Name:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ child.name }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Birth Date:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ formatDate(child.birth_date) }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Age:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ calculateAge(child.birth_date) }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Gender:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ child.gender || 'Not specified' }}</dd>
              </div>
            </dl>
          </div>
          
          <div>
            <h4 class="text-sm font-medium text-gray-500 mb-2">Birth Information</h4>
            <dl class="space-y-2">
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Birth Weight:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ child.birth_weight || 'N/A' }} kg</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-500">Birth Length:</dt>
                <dd class="text-sm font-medium text-gray-900">{{ child.birth_length || 'N/A' }} cm</dd>
              </div>
              <div v-if="child.birth_complications" class="col-span-2">
                <dt class="text-sm text-gray-500 mb-1">Birth Complications:</dt>
                <dd class="text-sm text-gray-900">{{ child.birth_complications }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      <!-- Vaccinations Tab -->
      <div v-else-if="activeTab === 'vaccinations'">
        <VaccinationTracker :child-id="child.id" />
      </div>

      <!-- Growth Tab -->
      <div v-else-if="activeTab === 'growth'">
        <GrowthChart :child-id="child.id" />
      </div>

      <!-- Milestones Tab -->
      <div v-else-if="activeTab === 'milestones'">
        <MilestoneChecker :child-id="child.id" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { calculateAge, formatDate } from '../../utils/dates'

// Import child-specific components
import VaccinationTracker from './VaccinationTracker.vue'
import GrowthChart from './GrowthChart.vue'
import MilestoneChecker from './MilestoneChecker.vue'

export default {
  name: 'ChildDetailsView',
  components: {
    VaccinationTracker,
    GrowthChart,
    MilestoneChecker
  },
  props: {
    child: {
      type: Object,
      required: true
    }
  },
  emits: ['close'],
  setup() {
    const activeTab = ref('info')
    
    const tabs = [
      { key: 'info', label: 'Basic Info' },
      { key: 'vaccinations', label: 'Vaccinations' },
      { key: 'growth', label: 'Growth' },
      { key: 'milestones', label: 'Milestones' }
    ]

    return {
      activeTab,
      tabs,
      calculateAge,
      formatDate
    }
  }
}
</script>