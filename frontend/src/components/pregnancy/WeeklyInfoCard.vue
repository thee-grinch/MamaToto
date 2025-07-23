<!-- src/components/pregnancy/WeeklyInfoCard.vue -->
<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Week {{ weeklyInfo.week }} Information</h3>
        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-pink-100 text-pink-800">
          Trimester {{ weeklyInfo.trimester }}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Baby Development -->
        <div>
          <h4 class="font-medium text-gray-900 mb-3 flex items-center">
            <svg class="h-5 w-5 text-pink-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            Baby Development
          </h4>
          <div class="bg-pink-50 p-4 rounded-lg">
            <p class="text-sm text-pink-800 mb-2">
              Your baby is about the size of a <strong>{{ weeklyInfo.baby_size }}</strong>
            </p>
            <p class="text-sm text-pink-700">
              This week, your baby is developing rapidly with important organ formation and growth.
            </p>
          </div>
        </div>

        <!-- Common Symptoms -->
        <div>
          <h4 class="font-medium text-gray-900 mb-3 flex items-center">
            <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Common Symptoms
          </h4>
          <div class="space-y-2">
            <div 
              v-for="symptom in weeklyInfo.symptoms" 
              :key="symptom"
              class="flex items-center text-sm text-gray-700"
            >
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
              {{ symptom }}
            </div>
          </div>
        </div>
      </div>

      <!-- Health Tips -->
      <div class="mt-6">
        <h4 class="font-medium text-gray-900 mb-3 flex items-center">
          <svg class="h-5 w-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Health Tips for This Week
        </h4>
        <div class="bg-green-50 p-4 rounded-lg">
          <ul class="space-y-2">
            <li 
              v-for="tip in weeklyInfo.tips" 
              :key="tip"
              class="flex items-start text-sm text-green-800"
            >
              <svg class="h-4 w-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ tip }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Recommended Appointments -->
      <div v-if="weeklyInfo.appointments && weeklyInfo.appointments.length > 0" class="mt-6">
        <h4 class="font-medium text-gray-900 mb-3 flex items-center">
          <svg class="h-5 w-5 text-purple-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Recommended This Week
        </h4>
        <div class="bg-purple-50 p-4 rounded-lg">
          <ul class="space-y-1">
            <li 
              v-for="appointment in weeklyInfo.appointments" 
              :key="appointment"
              class="text-sm text-purple-800"
            >
              • {{ appointment }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WeeklyInfoCard',
  props: {
    weeklyInfo: {
      type: Object,
      required: true
    }
  }
}
</script>