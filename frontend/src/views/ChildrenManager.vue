<!-- src/views/ChildrenManager.vue -->
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Children</h1>
        <p class="mt-1 text-sm text-gray-500">Manage your children's health records</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button
          @click="showAddChildForm = true"
          class="btn btn-primary"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Child
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <LoadingSpinner v-if="childrenStore.loading" size="large" message="Loading children data..." />

    <!-- Children List -->
    <div v-else-if="childrenStore.children.length > 0" class="space-y-6">
      <!-- Children Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <ChildCard
          v-for="child in childrenStore.children"
          :key="child.id"
          :child="child"
          @select="selectChild"
          @edit="editChild"
        />
      </div>

      <!-- Selected Child Details -->
      <div v-if="selectedChild" class="mt-8">
        <ChildDetailsView 
          :child="selectedChild"
          @close="selectedChild = null"
        />
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-red-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Overdue Vaccinations</p>
              <p class="text-2xl font-semibold text-gray-900">{{ childrenStore.overdueVaccinations.length }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Up to Date</p>
              <p class="text-2xl font-semibold text-gray-900">{{ upToDateCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="bg-blue-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Upcoming</p>
              <p class="text-2xl font-semibold text-gray-900">{{ childrenStore.upcomingVaccinations.length }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="mx-auto h-12 w-12 text-gray-400">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No children added</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by adding your first child.</p>
      <div class="mt-6">
        <button
          @click="showAddChildForm = true"
          class="btn btn-primary"
        >
          Add Your First Child
        </button>
      </div>
    </div>

    <!-- Add Child Modal -->
    <ChildForm
      v-if="showAddChildForm"
      @close="showAddChildForm = false"
      @saved="handleChildSaved"
    />

    <!-- Edit Child Modal -->
    <ChildForm
      v-if="showEditChildForm && editingChild"
      :child="editingChild"
      @close="showEditChildForm = false"
      @saved="handleChildSaved"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useChildrenStore } from '../stores/children'
import { calculateAge } from '../utils/dates'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

// Import child components
import ChildCard from '../components/child/ChildCard.vue'
import ChildDetailsView from '../components/child/ChildDetailsView.vue'
import ChildForm from '../components/forms/ChildForm.vue'

export default {
  name: 'ChildrenManager',
  components: {
    LoadingSpinner,
    ChildCard,
    ChildDetailsView,
    ChildForm
  },
  setup() {
    const childrenStore = useChildrenStore()
    const showAddChildForm = ref(false)
    const showEditChildForm = ref(false)
    const selectedChild = ref(null)
    const editingChild = ref(null)

    const upToDateCount = computed(() => {
      return childrenStore.children.length - childrenStore.overdueVaccinations.length
    })

    const selectChild = (child) => {
      selectedChild.value = child
      childrenStore.setSelectedChild(child)
      // Fetch detailed data for selected child
      childrenStore.fetchChildVaccinations(child.id)
      childrenStore.fetchChildGrowthRecords(child.id)
    }

    const editChild = (child) => {
      editingChild.value = child
      showEditChildForm.value = true
    }

    const handleChildSaved = () => {
      showAddChildForm.value = false
      showEditChildForm.value = false
      editingChild.value = null
      childrenStore.fetchChildren()
    }

    onMounted(() => {
      childrenStore.fetchChildren()
    })

    return {
      childrenStore,
      showAddChildForm,
      showEditChildForm,
      selectedChild,
      editingChild,
      upToDateCount,
      selectChild,
      editChild,
      handleChildSaved,
      calculateAge
    }
  }
}
</script>