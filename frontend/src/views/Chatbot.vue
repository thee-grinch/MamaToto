<!-- src/views/Chatbot.vue -->
<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center">
        <div class="bg-purple-100 rounded-full p-2">
          <svg class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <div class="ml-3">
          <h1 class="text-lg font-semibold text-gray-900">Health Assistant</h1>
          <p class="text-sm text-gray-500">Ask me about maternal and child health</p>
        </div>
      </div>
    </div>

    <!-- Chat Messages -->
    <div class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50" ref="messagesContainer">
      <!-- Welcome Message -->
      <div v-if="messages.length === 0" class="text-center py-8">
        <div class="bg-white rounded-lg p-6 shadow-sm max-w-md mx-auto">
          <div class="bg-purple-100 rounded-full p-3 w-16 h-16 mx-auto mb-4">
            <svg class="h-10 w-10 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Welcome to your Health Assistant!</h3>
          <p class="text-gray-600 mb-4">I'm here to help answer your questions about pregnancy, child health, vaccinations, and more.</p>
          
          <!-- Quick Questions -->
          <div class="space-y-2">
            <p class="text-sm font-medium text-gray-700 mb-2">Try asking:</p>
            <button
              v-for="suggestion in quickQuestions"
              :key="suggestion"
              @click="sendMessage(suggestion)"
              class="block w-full text-left px-3 py-2 text-sm text-purple-600 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>
      </div>

      <!-- Chat Messages -->
      <div v-for="message in messages" :key="message.id" class="flex" :class="message.type === 'user' ? 'justify-end' : 'justify-start'">
        <div class="max-w-xs lg:max-w-md">
          <!-- User Message -->
          <div v-if="message.type === 'user'" class="bg-pink-500 text-white rounded-lg px-4 py-2">
            <p class="text-sm">{{ message.content }}</p>
          </div>
          
          <!-- Bot Message -->
          <div v-else class="bg-white rounded-lg px-4 py-3 shadow-sm border">
            <div class="flex items-start space-x-2">
              <div class="bg-purple-100 rounded-full p-1 flex-shrink-0">
                <svg class="h-4 w-4 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-sm text-gray-900">{{ message.content }}</p>
                <p v-if="message.disclaimer" class="text-xs text-gray-500 mt-2 italic">
                  {{ message.disclaimer }}
                </p>
              </div>
            </div>
          </div>
          
          <p class="text-xs text-gray-500 mt-1" :class="message.type === 'user' ? 'text-right' : 'text-left'">
            {{ formatTime(message.timestamp) }}
          </p>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isTyping" class="flex justify-start">
        <div class="bg-white rounded-lg px-4 py-3 shadow-sm border max-w-xs">
          <div class="flex items-center space-x-1">
            <div class="bg-purple-100 rounded-full p-1">
              <svg class="h-4 w-4 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="bg-white border-t border-gray-200 p-4">
      <div class="flex space-x-4">
        <div class="flex-1">
          <input
            v-model="newMessage"
            @keypress.enter="sendUserMessage"
            type="text"
            placeholder="Ask me about pregnancy, child health, vaccinations..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            :disabled="isTyping"
          />
        </div>
        <button
          @click="sendUserMessage"
          :disabled="!newMessage.trim() || isTyping"
          class="btn btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick, onMounted } from 'vue'
import { useHealthStore } from '../stores/health'

export default {
  name: 'Chatbot',
  setup() {
    const healthStore = useHealthStore()
    const messages = ref([])
    const newMessage = ref('')
    const isTyping = ref(false)
    const messagesContainer = ref(null)

    const quickQuestions = [
      "What vaccinations does my child need?",
      "When should I see a doctor during pregnancy?",
      "What are the warning signs during pregnancy?",
      "How can I track my child's growth?",
      "What should I eat during pregnancy?"
    ]

    const sendMessage = (message) => {
      newMessage.value = message
      sendUserMessage()
    }

    const sendUserMessage = async () => {
      if (!newMessage.value.trim()) return

      const userMessage = {
        id: Date.now(),
        type: 'user',
        content: newMessage.value,
        timestamp: new Date()
      }

      messages.value.push(userMessage)
      const query = newMessage.value
      newMessage.value = ''

      // Scroll to bottom
      await nextTick()
      scrollToBottom()

      // Show typing indicator
      isTyping.value = true

      try {
        // Get response from chatbot API
        const response = await healthStore.chatbotQuery(query)
        
        // Simulate typing delay
        setTimeout(() => {
          isTyping.value = false
          
          const botMessage = {
            id: Date.now() + 1,
            type: 'bot',
            content: response.response,
            disclaimer: response.disclaimer,
            timestamp: new Date()
          }

          messages.value.push(botMessage)
          
          // Scroll to bottom
          nextTick(() => scrollToBottom())
        }, 1500)

      } catch (error) {
        isTyping.value = false
        
        const errorMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: "I'm sorry, I'm having trouble responding right now. Please try again later or consult with a healthcare provider for any urgent concerns.",
          timestamp: new Date()
        }

        messages.value.push(errorMessage)
        nextTick(() => scrollToBottom())
      }
    }

    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    return {
      messages,
      newMessage,
      isTyping,
      messagesContainer,
      quickQuestions,
      sendMessage,
      sendUserMessage,
      formatTime
    }
  }
}
</script>
