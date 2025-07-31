// src/stores/user.js
import { defineStore } from 'pinia'
import api from '../utils/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),

  getters: {
    fullName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name || ''} ${state.user.last_name || ''}`.trim()
    },
    
    initials: (state) => {
      if (!state.user) return ''
      const first = state.user.first_name?.[0] || ''
      const last = state.user.last_name?.[0] || ''
      return (first + last).toUpperCase()
    }
  },

  actions: {
    async login(email, password) {
      try {
        this.loading = true
        this.error = null
        
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)
        
        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })
        
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        this.isAuthenticated = true
        
        await this.fetchUserData()
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.post('/auth/register', userData)
        
        // Auto-login after registration
        const loginSuccess = await this.login(userData.email, userData.password)
        return loginSuccess
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUserData() {
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch (error) {
        console.error('Error fetching user data:', error)
        this.logout()
      }
    },

    async updateProfile(profileData) {
      try {
        this.loading = true
        this.error = null
        
        const response = await api.put('/auth/me', profileData)
        this.user = response.data
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Profile update failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async changePassword(passwordData) {
      try {
        this.loading = true
        this.error = null
        
        // Assuming your backend has a PUT endpoint for changing password
        const response = await api.put('/auth/change-password', passwordData)
        
        // Optionally, handle success message or re-authentication if needed
        console.log('Password changed successfully', response.data);
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Password change failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async deleteAccount() {
      try {
        this.loading = true
        this.error = null
        
        // Assuming your backend has a DELETE endpoint for account deletion
        await api.delete('/auth/me')
        
        // Log out the user after successful deletion
        this.logout()
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Account deletion failed'
        return false
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
      this.token = null
      localStorage.removeItem('token')
    },

    clearError() {
      this.error = null
    },

    initializeAuth() {
      if (this.token) {
        this.isAuthenticated = true
        this.fetchUserData()
      }
    }
  }
})