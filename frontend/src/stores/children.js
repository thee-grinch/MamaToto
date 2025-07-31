// src/stores/children.js
import { defineStore } from 'pinia'
import api from '../utils/api'

export const useChildrenStore = defineStore('children', {
  state: () => ({
    children: [],
    selectedChild: null,
    vaccinations: {},
    growthRecords: {},
    milestones: {},
    loading: false,
    error: null
  }),

  getters: {
    getChildVaccinations: (state) => (childId) => {
      return state.vaccinations[childId] || []
    },

    getChildGrowthRecords: (state) => (childId) => {
      return state.growthRecords[childId] || []
    },

    getChildMilestones: (state) => (childId) => {
      return state.milestones[childId] || []
    },

    overdueVaccinations: (state) => {
      const overdue = []
      Object.values(state.vaccinations).flat().forEach(vaccination => {
        if (vaccination.status === 'overdue') {
          overdue.push(vaccination)
        }
      })
      return overdue
    },

    upcomingVaccinations: (state) => {
      const today = new Date().toISOString().split('T')[0]
      const nextMonth = new Date()
      nextMonth.setMonth(nextMonth.getMonth() + 1)
      const nextMonthStr = nextMonth.toISOString().split('T')[0]

      const upcoming = [] // Initialize upcoming array
      Object.values(state.vaccinations).flat().forEach(vaccination => {
        if (vaccination.status === 'pending' &&
            vaccination.scheduled_date >= today &&
            vaccination.scheduled_date <= nextMonthStr) {
          upcoming.push(vaccination)
        }
      })
      return upcoming.slice(0, 5)
    }
  },

  actions: {
    async fetchChildren() {
      try {
        this.loading = true
        const response = await api.get('/children')
        this.children = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch children'
      } finally {
        this.loading = false
      }
    },

    async createChild(childData) {
      try {
        this.loading = true
        this.error = null

        const response = await api.post('/children', childData)
        this.children.push(response.data)

        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create child record'
        return null
      } finally {
        this.loading = false
      }
    },

    async updateChild(childId, updateData) {
      try {
        this.loading = true
        const response = await api.put(`/children/${childId}`, updateData)

        const index = this.children.findIndex(c => c.id === childId)
        if (index !== -1) {
          this.children[index] = response.data
        }

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update child'
        return false
      } finally {
        this.loading = false
      }
    },

    async deleteChild(childId) {
      try {
        this.loading = true
        this.error = null

        await api.delete(`/children/${childId}`)

        // Remove child from state
        this.children = this.children.filter(child => child.id !== childId)

        // Clear selected child if it was the one deleted
        if (this.selectedChild?.id === childId) {
          this.selectedChild = null;
        }

        // Remove associated vaccinations and growth records from state
        delete this.vaccinations[childId];
        delete this.growthRecords[childId];
        delete this.milestones[childId]; // Also remove milestones

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete child'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchChildVaccinations(childId) {
      try {
        // Assuming loading state for vaccinations if needed
        const response = await api.get(`/children/${childId}/vaccinations`)
        this.vaccinations[childId] = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch vaccinations'
      }
    },

    async createVaccination(childId, vaccinationData) {
      try {
        this.loading = true // Or a specific loading state for vaccinations
        const response = await api.post(`/children/${childId}/vaccinations`, vaccinationData)

        if (!this.vaccinations[childId]) {
          this.vaccinations[childId] = []
        }
        this.vaccinations[childId].push(response.data)

        return true // Indicate success
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create vaccination record'
        return false // Indicate failure
      } finally {
        this.loading = false // Or the specific loading state
      }
    },

    async updateVaccination(childId, vaccinationId, updateData) {
      try {
        this.loading = true // Or specific loading state
        const response = await api.put(`/children/${childId}/vaccinations/${vaccinationId}`, updateData)

        // Update in state
        const index = this.vaccinations[childId].findIndex(v => v.id === vaccinationId)
        if (index !== -1) {
          this.vaccinations[childId][index] = response.data
        }

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update vaccination'
        return false
      } finally {
        this.loading = false // Or specific loading state
      }
    },

    async deleteVaccination(childId, vaccinationId) {
      try {
        this.loading = true // Or specific loading state
        this.error = null

        await api.delete(`/children/${childId}/vaccinations/${vaccinationId}`)

        // Remove from state
        if (this.vaccinations[childId]) {
          this.vaccinations[childId] = this.vaccinations[childId].filter(v => v.id !== vaccinationId)
        }

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete vaccination'
        return false
      } finally {
        this.loading = false // Or specific loading state
      }
    },


    async fetchChildGrowthRecords(childId) {
      try {
         // Assuming loading state for growth records if needed
        const response = await api.get(`/children/${childId}/growth`)
        this.growthRecords[childId] = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch growth records'
      }
    },

    async createGrowthRecord(childId, growthData) {
      try {
        this.loading = true // Or specific loading state
        const response = await api.post(`/children/${childId}/growth`, growthData)

        if (!this.growthRecords[childId]) {
          this.growthRecords[childId] = []
        }
        this.growthRecords[childId].push(response.data)

        return true // Indicate success
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create growth record'
        return false // Indicate failure
      } finally {
        this.loading = false // Or specific loading state
      }
    },

    async updateGrowthRecord(childId, growthId, updateData) {
      try {
        this.loading = true // Or specific loading state
        const response = await api.put(`/children/${childId}/growth/${growthId}`, updateData)

        // Update in state
        const index = this.growthRecords[childId].findIndex(g => g.id === growthId)
        if (index !== -1) {
          this.growthRecords[childId][index] = response.data
        }

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update growth record'
        return false
      } finally {
        this.loading = false // Or specific loading state
      }
    },

    async deleteGrowthRecord(childId, growthId) {
      try {
        this.loading = true // Or specific loading state
        this.error = null

        await api.delete(`/children/${childId}/growth/${growthId}`)

        // Remove from state
        if (this.growthRecords[childId]) {
          this.growthRecords[childId] = this.growthRecords[childId].filter(g => g.id !== growthId)
        }

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete growth record'
        return false
      } finally {
        this.loading = false // Or specific loading state
      }
    },

    async fetchChildMilestones(childId) {
       try {
         // Assuming loading state for milestones if needed
        const response = await api.get(`/children/${childId}/milestones`)
        this.milestones[childId] = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch milestones'
      }
    },

    async updateMilestone(childId, milestoneId, updateData) {
        try {
            this.loading = true; // Or specific loading state
            const response = await api.put(`/children/${childId}/milestones/${milestoneId}`, updateData);

            // Update in state
            if (this.milestones[childId]) {
                const index = this.milestones[childId].findIndex(m => m.id === milestoneId);
                if (index !== -1) {
                    this.milestones[childId][index] = response.data;
                }
            }
            return true;
        } catch (error) {
            this.error = error.response?.data?.detail || 'Failed to update milestone';
            return false;
        } finally {
            this.loading = false; // Or specific loading state
        }
    },


    setSelectedChild(child) {
      this.selectedChild = child
    },

    clearError() {
      this.error = null
    }
  }
})