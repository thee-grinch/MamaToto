<!-- src/components/child/GrowthChart.vue -->
<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h4 class="text-lg font-medium text-gray-900">Growth Tracking</h4>
      <button
        @click="showAddRecordForm = true"
        class="btn btn-sm btn-primary"
      >
        Add Measurement
      </button>
    </div>

    <LoadingSpinner v-if="childrenStore.loading" size="medium" />

    <div v-else-if="growthRecords.length > 0" class="space-y-6">
      <!-- Growth Chart -->
      <div class="bg-white p-4 border rounded-lg">
        <canvas ref="chartCanvas" width="400" height="200"></canvas>
      </div>

      <!-- Latest Measurements -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-if="latestRecord" class="bg-blue-50 p-4 rounded-lg">
          <h5 class="font-medium text-blue-900 mb-2">Weight</h5>
          <p class="text-2xl font-bold text-blue-600">{{ latestRecord.weight }} kg</p>
          <p class="text-sm text-blue-700">{{ latestRecord.weight_percentile }}th percentile</p>
        </div>
        
        <div v-if="latestRecord" class="bg-green-50 p-4 rounded-lg">
          <h5 class="font-medium text-green-900 mb-2">Height</h5>
          <p class="text-2xl font-bold text-green-600">{{ latestRecord.height }} cm</p>
          <p class="text-sm text-green-700">{{ latestRecord.height_percentile }}th percentile</p>
        </div>
        
        <div v-if="latestRecord && latestRecord.bmi" class="bg-purple-50 p-4 rounded-lg">
          <h5 class="font-medium text-purple-900 mb-2">BMI</h5>
          <p class="text-2xl font-bold text-purple-600">{{ latestRecord.bmi }}</p>
          <p class="text-sm text-purple-700">{{ getBMICategory(latestRecord.bmi) }}</p>
        </div>
      </div>

      <!-- Growth Records Table -->
      <div class="bg-white border rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Age</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weight</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Height</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">BMI</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="record in growthRecords" :key="record.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(record.recorded_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ record.age_months }} months
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.weight || 'N/A' }} kg
                <span v-if="record.weight_percentile" class="text-xs text-gray-500">
                  ({{ record.weight_percentile }}th)
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.height || 'N/A' }} cm
                <span v-if="record.height_percentile" class="text-xs text-gray-500">
                  ({{ record.height_percentile }}th)
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ record.bmi || 'N/A' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No growth records</h3>
      <p class="mt-1 text-sm text-gray-500">Start tracking your child's growth measurements.</p>
    </div>

    <!-- Add Growth Record Form Modal -->
    <GrowthRecordForm
      v-if="showAddRecordForm"
      :child-id="childId"
      @close="showAddRecordForm = false"
      @saved="handleRecordSaved"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useChildrenStore } from '../../stores/children'
import { formatDate } from '../../utils/dates'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import GrowthRecordForm from '../forms/GrowthRecordForm.vue'

export default {
  name: 'GrowthChart',
  components: {
    LoadingSpinner,
    GrowthRecordForm
  },
  props: {
    childId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const childrenStore = useChildrenStore()
    const showAddRecordForm = ref(false)
    const chartCanvas = ref(null)

    const growthRecords = computed(() => {
      return childrenStore.getChildGrowthRecords(props.childId)
    })

    const latestRecord = computed(() => {
      if (growthRecords.value.length === 0) return null
      return growthRecords.value[growthRecords.value.length - 1]
    })

    const getBMICategory = (bmi) => {
      if (bmi < 18.5) return 'Underweight'
      if (bmi < 25) return 'Normal'
      if (bmi < 30) return 'Overweight'
      return 'Obese'
    }

    const drawGrowthChart = async () => {
      await nextTick()
      if (!chartCanvas.value || growthRecords.value.length === 0) return

      const ctx = chartCanvas.value.getContext('2d')
      const canvas = chartCanvas.value
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Simple chart implementation
      // In a real app, you'd use Chart.js or similar library
      ctx.fillStyle = '#f3f4f6'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      
      ctx.fillStyle = '#374151'
      ctx.font = '14px Inter'
      ctx.fillText('Growth Chart (Weight vs Age)', 20, 30)
      
      // Draw axes
      ctx.strokeStyle = '#6b7280'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(50, 50)
      ctx.lineTo(50, canvas.height - 50)
      ctx.lineTo(canvas.width - 50, canvas.height - 50)
      ctx.stroke()
      
      // Plot data points
      if (growthRecords.value.length > 1) {
        ctx.strokeStyle = '#3b82f6'
        ctx.lineWidth = 2
        ctx.beginPath()
        
        growthRecords.value.forEach((record, index) => {
          const x = 50 + (index / (growthRecords.value.length - 1)) * (canvas.width - 100)
          const y = canvas.height - 50 - (record.weight / 20) * (canvas.height - 100)
          
          if (index === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
          
          // Draw point
          ctx.fillStyle = '#3b82f6'
          ctx.beginPath()
          ctx.arc(x, y, 3, 0, 2 * Math.PI)
          ctx.fill()
        })
        
        ctx.stroke()
      }
    }

    const handleRecordSaved = () => {
      showAddRecordForm.value = false
      childrenStore.fetchChildGrowthRecords(props.childId)
    }

    onMounted(async () => {
      await childrenStore.fetchChildGrowthRecords(props.childId)
      drawGrowthChart()
    })

    return {
      childrenStore,
      showAddRecordForm,
      chartCanvas,
      growthRecords,
      latestRecord,
      getBMICategory,
      handleRecordSaved,
      formatDate
    }
  }
}
</script>