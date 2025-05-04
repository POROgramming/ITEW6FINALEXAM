import { ref, reactive } from 'vue'

// Create a reactive store
const toasts = ref([])
let nextId = 1

// Create and export the store
export const useToastStore = () => {
  // Add a new toast
  const addToast = (message, type = 'info', duration = 5000) => {
    // Limit number of toasts on mobile
    const isMobile = window.innerWidth < 768
    const maxToasts = isMobile ? 3 : 5
    
    // If we have too many toasts, remove the oldest ones
    if (toasts.value.length >= maxToasts) {
      const oldestToasts = [...toasts.value]
        .sort((a, b) => a.id - b.id)
        .slice(0, toasts.value.length - maxToasts + 1)
      
      oldestToasts.forEach(toast => {
        removeToast(toast.id)
      })
    }
    
    const id = nextId++
    const toast = reactive({
      id,
      message,
      type,
      visible: false,
      duration: isMobile ? Math.min(duration, 4000) : duration // Shorter duration on mobile
    })
    
    toasts.value.push(toast)
    
    // Delay to trigger animation
    setTimeout(() => {
      toast.visible = true
    }, 10)
    
    // Auto-remove after duration
    setTimeout(() => {
      removeToast(id)
    }, toast.duration)
    
    return id
  }

  // Remove a toast by id
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    
    if (index !== -1) {
      // Trigger exit animation
      toasts.value[index].visible = false
      
      // Remove after animation completes
      setTimeout(() => {
        toasts.value = toasts.value.filter(toast => toast.id !== id)
      }, 300)
    }
  }

  // Helper methods for different toast types
  const success = (message, duration) => addToast(message, 'success', duration)
  const error = (message, duration) => addToast(message, 'error', duration)
  const warning = (message, duration) => addToast(message, 'warning', duration)
  const info = (message, duration) => addToast(message, 'info', duration)

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
}

// Export a direct useToast function for convenience
export const useToast = useToastStore