// frontend/src/stores/pregnancy.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const usePregnancyStore = defineStore('pregnancy', {
  state: () => ({
    pregnancies: [],
    activePregnancy: null, // To hold the currently selected or active pregnancy
    appointments: {}, // To store appointments keyed by pregnancy ID
    loading: false,
    error: null
  }),
  actions: {
    async fetchPregnancies() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/pregnancies'); // Hypothetical API endpoint
        this.pregnancies = response.data;
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching pregnancies:', err);
        throw err;
      } finally {
        this.loading = false;
      }
    },
    setActivePregnancy(pregnancyId) {
      this.activePregnancy = this.pregnancies.find(p => p.id === pregnancyId) || null;
      // Optionally fetch appointments for the active pregnancy immediately
      if (this.activePregnancy && !this.appointments[pregnancyId]) {
        this.fetchAppointments(pregnancyId);
      }
    },
    async fetchAppointments(pregnancyId) {
      if (this.appointments[pregnancyId]) {
        // Appointments already in store for this pregnancy, no need to refetch
        return this.appointments[pregnancyId];
      }

      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/pregnancies/${pregnancyId}/appointments`); // Hypothetical API endpoint
        this.appointments[pregnancyId] = response.data;
        return response.data;
      } catch (err) {
        this.error = err.message;
        console.error(`Error fetching appointments for pregnancy ${pregnancyId}:`, err);
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async createAppointment(pregnancyId, appointmentData) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.post(`/api/pregnancies/${pregnancyId}/appointments`, appointmentData);
        // Add the new appointment to the state
        if (!this.appointments[pregnancyId]) {
          this.appointments[pregnancyId] = [];
        }
        this.appointments[pregnancyId].push(response.data);
        return response.data;
      } catch (err) {
        this.error = err.message;
        console.error(`Error creating appointment for pregnancy ${pregnancyId}:`, err);
        throw err;
      } finally {
        this.loading = false;
      }
    }
    // You can add more actions here, e.g., updateAppointment, deleteAppointment, addPregnancy
  },
  getters: {
    getAllPregnancies: (state) => state.pregnancies,
    getActivePregnancy: (state) => state.activePregnancy,
    getAppointmentsByPregnancyId: (state) => (pregnancyId) => {
      return state.appointments[pregnancyId] || [];
    }
  }
});
