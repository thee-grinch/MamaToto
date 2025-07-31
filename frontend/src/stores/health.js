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

    async updateHealthRecord(recordId, updateData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.put(`/health/records/${recordId}`, updateData)
        
        // Update in state
        const index = this.healthRecords.findIndex(record => record.id === recordId)
        if (index !== -1) {
          this.healthRecords[index] = response.data
        }
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update health record'
        return false
      } finally {
        this.loading = false
      }
    },

    async deleteHealthRecord(recordId) {
      try {
        this.loading = true
        this.error = null
        
        await api.delete(`/health/records/${recordId}`)
        
        // Remove from state
        this.healthRecords = this.healthRecords.filter(record => record.id !== recordId)
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete health record'
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

     async updateMentalHealthAssessment(assessmentId, updateData) {
      try {
        this.loading = true
        this.error = null

        const response = await api.put(`/health/mental-health/${assessmentId}`, updateData);

        // Update in state
        const index = this.mentalHealthAssessments.findIndex(assessment => assessment.id === assessmentId);
        if (index !== -1) {
          this.mentalHealthAssessments[index] = response.data;
        }

        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update mental health assessment';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async deleteMentalHealthAssessment(assessmentId) {
      try {
        this.loading = true;
        this.error = null;

        await api.delete(`/health/mental-health/${assessmentId}`);

        // Remove from state
        this.mentalHealthAssessments = this.mentalHealthAssessments.filter(assessment => assessment.id !== assessmentId);

        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete mental health assessment';
        return false;
      } finally {
        this.loading = false;
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

     async updateEmergencyContact(contactId, updateData) {
      try {
        this.loading = true;
        this.error = null;

        const response = await api.put(`/health/emergency-contacts/${contactId}`, updateData);

        // Update in state
        const index = this.emergencyContacts.findIndex(contact => contact.id === contactId);
        if (index !== -1) {
          this.emergencyContacts[index] = response.data;
        }

        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update emergency contact';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async deleteEmergencyContact(contactId) {
      try {
        this.loading = true;
        this.error = null;

        await api.delete(`/health/emergency-contacts/${contactId}`);

        // Remove from state
        this.emergencyContacts = this.emergencyContacts.filter(contact => contact.id !== contactId);

        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete emergency contact';
        return false;
      } finally {
        this.loading = false;
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