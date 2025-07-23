<!-- src/components/dashboard/StatCard.vue -->
<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div :class="iconClasses">
            <component :is="iconComponent" class="h-6 w-6" />
          </div>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
            <dd class="text-lg font-medium text-gray-900">{{ value }}</dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

// Icon components
const HeartIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
  </svg>`
}

const UsersIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
  </svg>`
}

const CalendarIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>`
}

const AlertIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
  </svg>`
}

export default {
  name: 'StatCard',
  components: {
    HeartIcon,
    UsersIcon,
    CalendarIcon,
    AlertIcon
  },
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    icon: {
      type: String,
      required: true,
      validator: (value) => ['heart', 'users', 'calendar', 'alert'].includes(value)
    },
    color: {
      type: String,
      default: 'gray',
      validator: (value) => ['pink', 'blue', 'green', 'red', 'gray'].includes(value)
    }
  },
  setup(props) {
    const iconComponent = computed(() => {
      const icons = {
        heart: 'HeartIcon',
        users: 'UsersIcon',
        calendar: 'CalendarIcon',
        alert: 'AlertIcon'
      }
      return icons[props.icon]
    })
    
    const iconClasses = computed(() => {
      const colors = {
        pink: 'bg-pink-500 text-white',
        blue: 'bg-blue-500 text-white',
        green: 'bg-green-500 text-white',
        red: 'bg-red-500 text-white',
        gray: 'bg-gray-500 text-white'
      }
      
      return `p-3 rounded-md ${colors[props.color]}`
    })
    
    return {
      iconComponent,
      iconClasses
    }
  }
}
</script>