<!-- src/components/common/AlertMessage.vue -->
<template>
  <transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 transform translate-y-2"
    enter-to-class="opacity-100 transform translate-y-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100 transform translate-y-0"
    leave-to-class="opacity-0 transform translate-y-2"
  >
    <div v-if="visible" :class="alertClasses">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <component :is="iconComponent" class="h-5 w-5" />
        </div>
        <div class="ml-3 flex-1">
          <h3 v-if="title" :class="titleClasses">{{ title }}</h3>
          <div :class="messageClasses">
            <p>{{ message }}</p>
          </div>
        </div>
        <div class="ml-4 flex-shrink-0 flex">
          <button
            @click="closeAlert"
            :class="closeButtonClasses"
            type="button"
          >
            <span class="sr-only">Close</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

// Icon components
const SuccessIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
  </svg>`
}

const ErrorIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
  </svg>`
}

const WarningIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
  </svg>`
}

const InfoIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
  </svg>`
}

export default {
  name: 'AlertMessage',
  components: {
    SuccessIcon,
    ErrorIcon,
    WarningIcon,
    InfoIcon
  },
  props: {
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      required: true
    },
    autoClose: {
      type: Boolean,
      default: true
    },
    duration: {
      type: Number,
      default: 5000
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const visible = ref(true)
    
    const typeStyles = {
      success: {
        container: 'bg-green-50 border-green-200',
        icon: 'text-green-400',
        title: 'text-green-800',
        message: 'text-green-700',
        close: 'text-green-500 hover:text-green-600'
      },
      error: {
        container: 'bg-red-50 border-red-200',
        icon: 'text-red-400',
        title: 'text-red-800',
        message: 'text-red-700',
        close: 'text-red-500 hover:text-red-600'
      },
      warning: {
        container: 'bg-yellow-50 border-yellow-200',
        icon: 'text-yellow-400',
        title: 'text-yellow-800',
        message: 'text-yellow-700',
        close: 'text-yellow-500 hover:text-yellow-600'
      },
      info: {
        container: 'bg-blue-50 border-blue-200',
        icon: 'text-blue-400',
        title: 'text-blue-800',
        message: 'text-blue-700',
        close: 'text-blue-500 hover:text-blue-600'
      }
    }
    
    const alertClasses = computed(() => {
      return `fixed top-4 right-4 max-w-md w-full border rounded-lg p-4 shadow-lg z-50 ${typeStyles[props.type].container}`
    })
    
    const iconComponent = computed(() => {
      const components = {
        success: 'SuccessIcon',
        error: 'ErrorIcon',
        warning: 'WarningIcon',
        info: 'InfoIcon'
      }
      return components[props.type]
    })
    
    const titleClasses = computed(() => {
      return `text-sm font-medium ${typeStyles[props.type].title}`
    })
    
    const messageClasses = computed(() => {
      return `text-sm ${props.title ? 'mt-1' : ''} ${typeStyles[props.type].message}`
    })
    
    const closeButtonClasses = computed(() => {
      return `inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent ${typeStyles[props.type].close}`
    })
    
    const closeAlert = () => {
      visible.value = false
      setTimeout(() => emit('close'), 200)
    }
    
    onMounted(() => {
      if (props.autoClose) {
        setTimeout(closeAlert, props.duration)
      }
    })
    
    return {
      visible,
      alertClasses,
      iconComponent,
      titleClasses,
      messageClasses,
      closeButtonClasses,
      closeAlert
    }
  }
}
</script>