// frontend/src/stores/health.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useHealthStore = defineStore('health', {
  state: () => ({
    dashboardData: null,
    emergencyContacts: [], // Assuming the health store manages emergency contacts
    loading: false,
    error: null,
    loadingEmergencyContacts: false, // Dedicated loading for contacts
    errorEmergencyContacts: null // Dedicated error for contacts
  }),
  actions: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/dashboard'); // Hypothetical API endpoint for dashboard data
        this.dashboardData = response.data;
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching dashboard data:', err);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async fetchEmergencyContacts() {
        this.loadingEmergencyContacts = true;
        this.errorEmergencyContacts = null;
        try {
            const response = await axios.get('/api/emergency-contacts'); // Hypothetical API endpoint
            this.emergencyContacts = response.data;
        } catch (err) {
            this.errorEmergencyContacts = err.message;
            console.error('Error fetching emergency contacts:', err);
            throw err;
        } finally {
            this.loadingEmergencyContacts = false;
        }
    },

    async saveEmergencyContact(contactData) {
        this.loadingEmergencyContacts = true;
        this.errorEmergencyContacts = null;
        try {
            // Determine if it's a new contact or an update based on whether contactData has an ID
            const method = contactData.id ? 'put' : 'post';
            const url = contactData.id ? `/api/emergency-contacts/${contactData.id}` : '/api/emergency-contacts';
            const response = await axios[method](url, contactData);

            // Update the state with the saved contact
            if (method === 'post') {
                this.emergencyContacts.push(response.data);
            } else {
                const index = this.emergencyContacts.findIndex(contact => contact.id === response.data.id);
                if (index !== -1) {
                    this.emergencyContacts.splice(index, 1, response.data);
                }
            }
            return response.data; // Return the saved contact data
        } catch (err) {
            this.errorEmergencyContacts = err.message;
            console.error('Error saving emergency contact:', err);
            throw err;
        } finally {
            this.loadingEmergencyContacts = false;
        }
    }
    // You can add more actions here, e.g., deleteEmergencyContact, addHealthRecord, etc.
  },
  getters: {
    getDashboardData: (state) => state.dashboardData,
    getEmergencyContacts: (state) => state.emergencyContacts,
    getEmergencyContactById: (state) => (contactId) => {
        return state.emergencyContacts.find(contact => contact.id === contactId) || null;
    }
  }
});
