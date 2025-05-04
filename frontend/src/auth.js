import { reactive } from 'vue'
import axios from './axios'

export const auth = reactive({
  isLoggedIn: !!localStorage.getItem('access'),
  isStaff: localStorage.getItem('is_staff') === 'true',
  
  // Add token expiration check
  async checkTokenValidity() {
    const token = localStorage.getItem('access')
    if (!token) return false
    
    try {
      // Try to make a request to check if token is still valid
      await axios.get('user/')
      return true
    } catch (error) {
      // If we get an error, token is invalid or expired
      console.log('Token invalid or expired, logging out')
      this.logout()
      return false
    }
  },
  
  // Add logout method
  logout() {
    const cart = localStorage.getItem('cart')
    localStorage.clear()
    if (cart) localStorage.setItem('cart', cart)
    
    this.isLoggedIn = false
    this.isStaff = false
    
    // Redirect to login if not already there
    if (window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
  }
})

// Set up interceptor to check token on each request
axios.interceptors.response.use(
  response => response,
  error => {
    // If we get a 401 Unauthorized error, log out
    if (error.response && error.response.status === 401) {
      auth.logout()
    }
    return Promise.reject(error)
  }
)

// Check token validity periodically
setInterval(() => {
  if (auth.isLoggedIn) {
    auth.checkTokenValidity()
  }
}, 60000) // Check every minute