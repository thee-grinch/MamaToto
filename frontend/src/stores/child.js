// frontend/src/stores/child.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useChildStore = defineStore('child', {
  state: () => ({
    children: {}, // Store child details by ID
    milestones: {}, // Store milestones by child ID
    loading: false,
    error: null
  }),
  actions: {
    async fetchChildDetails(childId) {
      if (this.children[childId]) {
        // Child details already in store, no need to refetch
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
        // Milestones already in store, no need to refetch
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
    }
    // You can add more actions here, e.g., addChild, updateMilestone, etc.
  },
  getters: {
    getChildDetails: (state) => (childId) => {
      return state.children[childId];
    },
    getChildMilestones: (state) => (childId) => {
      return state.milestones[childId];
    }
  }
});
