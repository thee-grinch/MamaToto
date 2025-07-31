<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Change Password
              </h3>
              <div class="mt-6 space-y-5">
                <div>
                  <label for="current-password" class="form-label">Current Password *</label>
                  <input
                    id="current-password"
                    v-model="form.current_password"
                    type="password"
                    required
                    class="form-input"
                  />
                </div>
                <div>
                  <label for="new-password" class="form-label">New Password *</label>
                  <input
                    id="new-password"
                    v-model="form.new_password"
                    type="password"
                    required
                    class="form-input"
                  />
                </div>
                <div>
                  <label for="confirm-password" class="form-label">Confirm New Password *</label>
                  <input
                    id="confirm-password"
                    v-model="form.confirm_password"
                    type="password"
                    required
                    class="form-input"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-pink-600 text-base font-medium text-white hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 sm:ml-3 sm:w-auto sm:text-sm"
            @click="changePassword"
          >
            Change Password
          </button>
          <button
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            @click="closeForm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';
import { useUserStore } from '../stores/user';

export default {
  name: 'ChangePasswordForm',
  setup(props, { emit }) {
    const userStore = useUserStore();
    const form = reactive({
      current_password: '',
      new_password: '',
      confirm_password: '',
    });

    const changePassword = async () => {
      // Basic validation (can be enhanced)
      if (!form.current_password || !form.new_password || !form.confirm_password) {
        alert('Please fill in all password fields.');
        return;
      }

      if (form.new_password !== form.confirm_password) {
        alert('New password and confirm password do not match.');
        return;
      }

      // Assuming an action in userStore to change password
      const success = await userStore.changePassword({
        current_password: form.current_password,
        new_password: form.new_password,
      });

      if (success) {
        emit('saved');
      }
    };

    const closeForm = () => {
      emit('close');
    };

    return {
      form,
      changePassword,
      closeForm,
    };
  },
};
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>