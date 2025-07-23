// src/stores/pregnancy.js
import { defineStore } from 'pinia'
import api from '../utils/api'

export const usePregnancyStore = defineStore('pregnancy', {
  state: () => ({
    pregnancies: [],
    activePregnancy: null,
    appointments: [],
    weeklyInfo: null,
    dangerSigns: [],
    loading: false,
    error: null
  }),

  getters: {
    currentWeek: (state) => {
      return state.activePregnancy?.current_week || null
    },
    
    trimester: (state) => {
      return state.activePregnancy?.trimester || null
    },
    
    dueDate: (state) => {
      return state.activePregnancy?.due_date || null
    },
    
    upcomingAppointments: (state) => {
      const today = new Date().toISOString().split('T')[0]
      return state.appointments.filter(apt => 
        apt.scheduled_date >= today && !apt.completed
      ).slice(0, 3)
    }
  },

  actions: {
    async fetchPregnancies() {
      try {
        this.loading = true
        const response = await api.get('/pregnancy')
        this.pregnancies = response.data
        
        // Set active pregnancy
        this.activePregnancy = this.pregnancies.find(p => p.is_active) || null
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch pregnancies'
      } finally {
        this.loading = false
      }
    },

    async createPregnancy(pregnancyData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.post('/pregnancy', pregnancyData)
        this.pregnancies.unshift(response.data)
        this.activePregnancy = response.data
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create pregnancy record'
        return false
      } finally {
        this.loading = false
      }
    },

    async updatePregnancy(pregnancyId, updateData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.put(`/pregnancy/${pregnancyId}`, updateData)
        
        // Update in list
        const index = this.pregnancies.findIndex(p => p.id === pregnancyId)
        if (index !== -1) {
          this.pregnancies[index] = response.data
        }
        
        // Update active pregnancy if it's the same one
        if (this.activePregnancy?.id === pregnancyId) {
          this.activePregnancy = response.data
        }
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update pregnancy'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAppointments() {
      try {
        const response = await api.get('/pregnancy/appointments')
        this.appointments = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch appointments'
      }
    },

    async createAppointment(appointmentData) {
      try {
        this.loading = true
        const response = await api.post('/pregnancy/appointments', appointmentData)
        this.appointments.push(response.data)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create appointment'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchWeeklyInfo() {
      if (!this.activePregnancy) return
      
      try {
        const response = await api.post('/pregnancy/weekly-info')
        this.weeklyInfo = response.data
      } catch (error) {
        console.error('Failed to fetch weekly info:', error)
      }
    },

    async fetchDangerSigns() {
      try {
        const response = await api.get('/pregnancy/danger-signs')
        this.dangerSigns = response.data.danger_signs
      } catch (error) {
        console.error('Failed to fetch danger signs:', error)
      }
    },

    clearError() {
      this.error = null
    }
  }
})