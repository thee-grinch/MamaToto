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
                {{ contact ? 'Edit Emergency Contact' : 'Add Emergency Contact' }}
              </h3>
              <div class="mt-6 space-y-5">
                <div>
                  <label for="name" class="form-label">Name</label>
                  <input type="text" name="name" id="name" v-model="form.name" class="form-input" />
                </div>
                <div>
                  <label for="relationship" class="form-label">Relationship</label>
                  <input type="text" name="relationship" id="relationship" v-model="form.relationship" class="form-input" />
                </div>
                <div>
                  <label for="phone" class="form-label">Phone Number</label>
                  <input type="text" name="phone" id="phone" v-model="form.phone" class="form-input" placeholder="+254 700 000 000" />
                </div>
                <div>
                  <label for="address" class="form-label">Address (Optional)</label>
                  <input type="text" name="address" id="address" v-model="form.address" class="form-input" placeholder="City, County" />
                </div>
                 <div class="flex items-center">
                    <input id="is_primary" name="is_primary" type="checkbox" v-model="form.is_primary" class="form-checkbox h-4 w-4 text-pink-600 transition duration-150 ease-in-out" />
                    <label for="is_primary" class="ml-2 block text-sm leading-5 text-gray-900">Primary Contact</label>
                  </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-pink-600 text-base font-medium text-white hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 sm:ml-3 sm:w-auto sm:text-sm"
            @click="saveContact"
          >
            {{ contact ? 'Update Contact' : 'Save Contact' }}
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
import { reactive, watch } from 'vue';
import { useHealthStore } from '../stores/health';

export default {
  name: 'EmergencyContactForm',
  props: {
    contact: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const healthStore = useHealthStore();
    const form = reactive({
      name: '',
      relationship: '',
      phone: '',
      address: '',
      is_primary: false,
    });

    const initializeForm = () => {
      if (props.contact) {
        Object.keys(form).forEach(key => {
          if (props.contact[key] !== undefined) {
            form[key] = props.contact[key];
          }
        });
      } else {
        // Reset form for adding new contact
        Object.keys(form).forEach(key => {
          form[key] = '';
        });
        form.is_primary = false;
      }
    };

    const saveContact = async () => {
      // Basic validation (can be enhanced)
      if (!form.name || !form.relationship || !form.phone) {
        alert('Please fill in name, relationship, and phone number.');
        return;
      }
      
      let success;
      if (props.contact) {
        success = await healthStore.updateEmergencyContact(props.contact.id, {
          name: form.name,
          relationship: form.relationship,
          phone: form.phone,
          address: form.address,
          is_primary: form.is_primary,
        });
      } else {
        success = await healthStore.createEmergencyContact({
          name: form.name,
          relationship: form.relationship,
          phone: form.phone,
          address: form.address,
          is_primary: form.is_primary,
        });
      }

      if (success) {
        emit('saved');
      }
    };

    const closeForm = () => {
      emit('close');
    };

    watch(() => props.contact, () => {
      initializeForm();
    });

    // Initialize form when component is created
    initializeForm();

    return {
      form,
      saveContact,
      closeForm,
    };
  },
};
</script>

<style scoped>
/* Add any component-specific styles here if needed */
</style>