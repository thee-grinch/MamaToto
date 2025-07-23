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
      const upcoming = []
      const today = new Date().toISOString().split('T')[0]
      const nextMonth = new Date()
      nextMonth.setMonth(nextMonth.getMonth() + 1)
      const nextMonthStr = nextMonth.toISOString().split('T')[0]
      
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

    async fetchChildVaccinations(childId) {
      try {
        const response = await api.get(`/children/${childId}/vaccinations`)
        this.vaccinations[childId] = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch vaccinations'
      }
    },

    async createVaccination(childId, vaccinationData) {
      try {
        this.loading = true
        const response = await api.post(`/children/${childId}/vaccinations`, vaccinationData)
        
        if (!this.vaccinations[childId]) {
          this.vaccinations[childId] = []
        }
        this.vaccinations[childId].push(response.data)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create vaccination record'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchChildGrowthRecords(childId) {
      try {
        const response = await api.get(`/children/${childId}/growth`)
        this.growthRecords[childId] = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch growth records'
      }
    },

    async createGrowthRecord(childId, growthData) {
      try {
        this.loading = true
        const response = await api.post(`/children/${childId}/growth`, growthData)
        
        if (!this.growthRecords[childId]) {
          this.growthRecords[childId] = []
        }
        this.growthRecords[childId].push(response.data)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create growth record'
        return false
      } finally {
        this.loading = false
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