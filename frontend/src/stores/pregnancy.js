// frontend/src/stores/pregnancy.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const usePregnancyStore = defineStore('pregnancy', {
  state: () => ({
    pregnancies: [],
    activePregnancy: null,
    appointments: {},
    loading: false,
    error: null,
    loadingAppointments: false,
    errorAppointments: null
  }),
  actions: {
    async fetchPregnancies() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/pregnancies');
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
      if (this.activePregnancy && !this.appointments[pregnancyId]) {
        this.fetchAppointments(pregnancyId);
      }
    },
    async fetchAppointments(pregnancyId) {
      if (this.appointments[pregnancyId]) {
        return this.appointments[pregnancyId];
      }

      this.loadingAppointments = true;
      this.errorAppointments = null;
      try {
        const response = await axios.get(`/api/pregnancies/${pregnancyId}/appointments`);
        this.appointments[pregnancyId] = response.data;
        return response.data;
      } catch (err) {
        this.errorAppointments = err.message;
        console.error(`Error fetching appointments for pregnancy ${pregnancyId}:`, err);
        throw err;
      } finally {
        this.loadingAppointments = false;
      }
    },
    async createAppointment(appointmentData) {
      this.loadingAppointments = true;
      this.errorAppointments = null;
      try {
        const response = await axios.post(`/api/pregnancies/${appointmentData.pregnancy_id}/appointments`, appointmentData);
        if (!this.appointments[appointmentData.pregnancy_id]) {
          this.appointments[appointmentData.pregnancy_id] = [];
        }
        this.appointments[appointmentData.pregnancy_id].push(response.data);
        return response.data;
      } catch (err) {
        this.errorAppointments = err.message;
        console.error(`Error creating appointment for pregnancy ${appointmentData.pregnancy_id}:`, err);
        throw err;
      } finally {
        this.loadingAppointments = false;
      }
    },

    async updateAppointment(appointmentId, appointmentData) {
        this.loadingAppointments = true;
        this.errorAppointments = null;
        try {
            const response = await axios.put(`/api/appointments/${appointmentId}`, appointmentData);
            for (const pregnancyId in this.appointments) {
                const index = this.appointments[pregnancyId].findIndex(appt => appt.id === response.data.id);
                if (index !== -1) {
                    this.appointments[pregnancyId].splice(index, 1, response.data);
                    break;
                }
            }
            return response.data;
        } catch (err) {
            this.errorAppointments = err.message;
            console.error(`Error updating appointment ${appointmentId}:`, err);
            throw err;
        } finally {
            this.loadingAppointments = false;
        }
    }
  },
  getters: {
    getAllPregnancies: (state) => state.pregnancies,
    getActivePregnancy: (state) => state.activePregnancy,
    getAppointmentsByPregnancyId: (state) => (pregnancyId) => {
      return state.appointments[pregnancyId] || [];
    }
  }
});
