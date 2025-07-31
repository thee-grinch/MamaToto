// frontend/src/stores/child.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useChildStore = defineStore('child', {
  state: () => ({
    children: {}, // Store child details by ID
    milestones: {}, // Store milestones by child ID
    growthRecords: {}, // Add state for growth records
    loading: false,
    error: null,
    loadingGrowthRecords: false,
    errorGrowthRecords: null
  }),
  actions: {
    async fetchChildDetails(childId) {
      if (this.children[childId]) {
        return this.children[childId];
      }

      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/children/${childId}`);
        this.children[childId] = response.data;
        return response.data;
      } catch (err) {
        this.error = err.message;
        console.error(`Error fetching child details for ${childId}:`, err);
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchChildMilestones(childId) {
       if (this.milestones[childId]) {
        return this.milestones[childId];
      }

      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/children/${childId}/milestones`);
        this.milestones[childId] = response.data;
        return response.data;
      } catch (err) {
        this.error = err.message;
        console.error(`Error fetching child milestones for ${childId}:`, err);
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async fetchChildGrowthRecords(childId) {
        this.loadingGrowthRecords = true;
        this.errorGrowthRecords = null;
        try {
            const response = await axios.get(`/api/children/${childId}/growth-records`);
            this.growthRecords[childId] = response.data;
            return response.data;
        } catch (err) {
            this.errorGrowthRecords = err.message;
            console.error(`Error fetching growth records for child ${childId}:`, err);
            throw err;
        } finally {
            this.loadingGrowthRecords = false;
        }
    },

    async addGrowthRecord(childId, recordData) {
        this.loadingGrowthRecords = true;
        this.errorGrowthRecords = null;
        try {
            const response = await axios.post(`/api/children/${childId}/growth-records`, recordData);
            if (!this.growthRecords[childId]) {
                this.growthRecords[childId] = [];
            }
            this.growthRecords[childId].push(response.data);
            this.growthRecords[childId].sort((a, b) => new Date(a.recorded_date) - new Date(b.recorded_date));
            return response.data;
        } catch (err) {
            this.errorGrowthRecords = err.message;
            console.error(`Error adding growth record for child ${childId}:`, err);
            throw err;
        } finally {
            this.loadingGrowthRecords = false;
        }
    }
  },
  getters: {
    getChildDetails: (state) => (childId) => {
      return state.children[childId];
    },
    getChildMilestones: (state) => (childId) => {
      return state.milestones[childId];
    },
    getChildGrowthRecords: (state) => (childId) => {
        return state.growthRecords[childId] || [];
    }
  }
});
