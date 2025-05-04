export function useToast() {
    /**
     * Show a toast notification
     * @param {string} type - Type of toast: 'success', 'error', 'warning', 'info'
     * @param {string} message - Message to display
     * @param {number} duration - Duration in milliseconds
     */
    const showToast = (type, message, duration = 3000) => {
      // Check if Vue root instance is available
      if (window.$root) {
        window.$root.$emit('show-toast', type, message, duration);
      } else {
        console.warn('Toast system not available: $root not found');
      }
    };
  
    return {
      showToast
    };
  }