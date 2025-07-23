<!-- src/components/common/LoadingSpinner.vue -->
<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses">
      <div class="animate-spin rounded-full border-t-2 border-b-2 border-current"></div>
    </div>
    <p v-if="message" :class="textClasses">{{ message }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'LoadingSpinner',
  props: {
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    message: {
      type: String,
      default: ''
    },
    overlay: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const containerClasses = computed(() => {
      const base = 'flex flex-col items-center justify-center'
      return props.overlay 
        ? `${base} fixed inset-0 bg-black bg-opacity-50 z-50`
        : `${base} p-4`
    })
    
    const spinnerClasses = computed(() => {
      const sizes = {
        small: 'h-6 w-6',
        medium: 'h-8 w-8',
        large: 'h-12 w-12'
      }
      
      return `${sizes[props.size]} text-pink-600`
    })
    
    const textClasses = computed(() => {
      const sizes = {
        small: 'text-sm',
        medium: 'text-base',
        large: 'text-lg'
      }
      
      return `mt-2 ${sizes[props.size]} text-gray-600`
    })
    
    return {
      containerClasses,
      spinnerClasses,
      textClasses
    }
  }
}
</script>