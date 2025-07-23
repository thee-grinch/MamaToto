<!-- src/views/Profile.vue -->
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Profile Settings</h1>
      <p class="mt-1 text-sm text-gray-500">Manage your account information and preferences</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile Form -->
      <div class="lg:col-span-2">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Personal Information</h3>
            
            <form @submit.prevent="handleUpdateProfile" class="space-y-6">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label for="first_name" class="form-label">First Name</label>
                  <input
                    id="first_name"
                    v-model="profileForm.first_name"
                    type="text"
                    class="form-input"
                  />
                </div>
                
                <div>
                  <label for="last_name" class="form-label">Last Name</label>
                  <input
                    id="last_name"
                    v-model="profileForm.last_name"
                    type="text"
                    class="form-input"
                  />
                </div>
              </div>
              
              <div>
                <label for="email" class="form-label">Email Address</label>
                <input
                  id="email"
                  v-model="profileForm.email"
                  type="email"
                  disabled
                  class="form-input bg-gray-50 cursor-not-allowed"
                />
                <p class="mt-1 text-sm text-gray-500">Email cannot be changed</p>
              </div>
              
              <div>
                <label for="phone" class="form-label">Phone Number</label>
                <input
                  id="phone"
                  v-model="profileForm.phone"
                  type="tel"
                  class="form-input"
                  placeholder="+254 700 000 000"
                />
              </div>
              
              <div>
                <label for="location" class="form-label">Location</label>
                <input
                  id="location"
                  v-model="profileForm.location"
                  type="text"
                  class="form-input"
                  placeholder="City, County"
                />
              </div>
              
              <div>
                <label for="preferred_language" class="form-label">Preferred Language</label>
                <select
                  id="preferred_language"
                  v-model="profileForm.preferred_language"
                  class="form-input"
                >
                  <option value="en">English</option>
                  <option value="sw">Kiswahili</option>
                </select>
              </div>
              
              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="userStore.loading"
                  class="btn btn-primary"
                >
                  <LoadingSpinner v-if="userStore.loading" size="small" class="mr-2" />
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Profile Summary & Actions -->
      <div class="space-y-6">
        <!-- Profile Card -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6 text-center">
            <div class="mx-auto h-20 w-20 rounded-full bg-pink-500 flex items-center justify-center text-white text-2xl font-bold mb-4">
              {{ userStore.initials }}
            </div>
            <h3 class="text-lg font-medium text-gray-900">{{ userStore.fullName || 'User' }}</h3>
            <p class="text-sm text-gray-500">{{ userStore.user?.email }}</p>
            <p class="text-sm text-gray-500 mt-1">
              Member since {{ formatDate(userStore.user?.created_at) }}
            </p>
          </div>
        </div>

        <!-- Emergency Contacts -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900">Emergency Contacts</h3>
              <button
                @click="showEmergencyContactForm = true"
                class="btn btn-sm btn-outline"
              >
                Add Contact
              </button>
            </div>
            
            <div v-if="healthStore.emergencyContacts.length > 0" class="space-y-3">
              <div
                v-for="contact in healthStore.emergencyContacts"
                :key="contact.id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ contact.name }}</p>
                  <p class="text-sm text-gray-500">{{ contact.relationship }}</p>
                  <p class="text-sm text-gray-600">{{ contact.phone }}</p>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="contact.is_primary" class="badge badge-success text-xs">Primary</span>
                  <button class="text-gray-400 hover:text-gray-600">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-4">
              <p class="text-sm text-gray-500">No emergency contacts added</p>
            </div>
          </div>
        </div>

        <!-- Account Actions -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Account Actions</h3>
            <div class="space-y-3">
              <button
                @click="showChangePasswordForm = true"
                class="w-full btn btn-outline text-left"
              >
                <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2l-4.586-4.586a2 2 0 010-2.828L8.828 3.172a2 2 0 012.828 0L15 7zM3 21h18M9 7h1m0 0v1" />
                </svg>
                Change Password
              </button>
              
              <button
                @click="exportData"
                class="w-full btn btn-outline text-left"
              >
                <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Export My Data
              </button>
              
              <button
                @click="confirmDeleteAccount"
                class="w-full btn btn-danger text-left"
              >
                <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Emergency Contact Form Modal -->
    <EmergencyContactForm
      v-if="showEmergencyContactForm"
      @close="showEmergencyContactForm = false"
      @saved="handleEmergencyContactSaved"
    />

    <!-- Change Password Modal -->
    <ChangePasswordForm
      v-if="showChangePasswordForm"
      @close="showChangePasswordForm = false"
      @saved="handlePasswordChanged"
    />
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useHealthStore } from '../stores/health'
import { formatDate } from '../utils/dates'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

// Import form components
import EmergencyContactForm from '../components/forms/EmergencyContactForm.vue'
import ChangePasswordForm from '../components/forms/ChangePasswordForm.vue'

export default {
  name: 'Profile',
  components: {
    LoadingSpinner,
    EmergencyContactForm,
    ChangePasswordForm
  },
  setup() {
    const userStore = useUserStore()
    const healthStore = useHealthStore()
    
    const showEmergencyContactForm = ref(false)
    const showChangePasswordForm = ref(false)
    
    const profileForm = reactive({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      location: '',
      preferred_language: 'en'
    })

    const initializeForm = () => {
      if (userStore.user) {
        Object.keys(profileForm).forEach(key => {
          profileForm[key] = userStore.user[key] || ''
        })
      }
    }

    const handleUpdateProfile = async () => {
      const success = await userStore.updateProfile(profileForm)
      if (success) {
        // Show success message
        console.log('Profile updated successfully')
      }
    }

    const handleEmergencyContactSaved = () => {
      showEmergencyContactForm.value = false
      healthStore.fetchEmergencyContacts()
    }

    const handlePasswordChanged = () => {
      showChangePasswordForm.value = false
      // Show success message
      console.log('Password changed successfully')
    }

    const exportData = () => {
      // TODO: Implement data export
      console.log('Export user data')
    }

    const confirmDeleteAccount = () => {
      if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        // TODO: Implement account deletion
        console.log('Delete account')
      }
    }

    onMounted(() => {
      initializeForm()
      healthStore.fetchEmergencyContacts()
    })

    return {
      userStore,
      healthStore,
      profileForm,
      showEmergencyContactForm,
      showChangePasswordForm,
      handleUpdateProfile,
      handleEmergencyContactSaved,
      handlePasswordChanged,
      exportData,
      confirmDeleteAccount,
      formatDate
    }
  }
}
</script>