// src/stores/health.js
import { defineStore } from 'pinia'
import api from '../utils/api'

export const useHealthStore = defineStore('health', {
  state: () => ({
    healthRecords: [],
    mentalHealthAssessments: [],
    emergencyContacts: [],
    dashboardData: null,
    loading: false,
    error: null
  }),

  getters: {
    recentHealthRecords: (state) => {
      return state.healthRecords
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5)
    },
    
    criticalRecords: (state) => {
      return state.healthRecords.filter(record => 
        record.severity === 'critical' || record.severity === 'high'
      )
    },
    
    primaryEmergencyContact: (state) => {
      return state.emergencyContacts.find(contact => contact.is_primary) || 
             state.emergencyContacts[0] || null
    }
  },

  actions: {
    async fetchDashboardData() {
      try {
        this.loading = true
        const response = await api.get('/dashboard')
        this.dashboardData = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch dashboard data'
      } finally {
        this.loading = false
      }
    },

    async fetchHealthRecords() {
      try {
        const response = await api.get('/health/records')
        this.healthRecords = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch health records'
      }
    },

    async createHealthRecord(recordData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.post('/health/records', recordData)
        this.healthRecords.unshift(response.data)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create health record'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchMentalHealthAssessments() {
      try {
        const response = await api.get('/health/mental-health')
        this.mentalHealthAssessments = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch assessments'
      }
    },

    async createMentalHealthAssessment(assessmentData) {
      try {
        this.loading = true
        const response = await api.post('/health/mental-health', assessmentData)
        this.mentalHealthAssessments.unshift(response.data)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to save assessment'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchEmergencyContacts() {
      try {
        const response = await api.get('/health/emergency-contacts')
        this.emergencyContacts = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch emergency contacts'
      }
    },

    async createEmergencyContact(contactData) {
      try {
        this.loading = true
        const response = await api.post('/health/emergency-contacts', contactData)
        this.emergencyContacts.push(response.data)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create emergency contact'
        return false
      } finally {
        this.loading = false
      }
    },

    async chatbotQuery(query) {
      try {
        this.loading = true
        const response = await api.post('/chatbot', null, {
          params: { query }
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Chatbot query failed'
        return null
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})