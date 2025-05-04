<template>
  <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container">
        <router-link
          class="navbar-brand"
          :to="auth.isLoggedIn ? (auth.isStaff ? '/monitor' : '/products') : '/login'"
        >
          <i class="bi bi-bag-heart-fill me-2"></i>E-Store
        </router-link>

        <button 
          class="navbar-toggler" 
          type="button" 
          @click="toggleNavbar"
          aria-controls="navbarContent" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent" ref="navbarCollapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- STAFF NAVIGATION -->
            <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
              <router-link class="nav-link" to="/monitor-products" @click="closeNavbar">
                <i class="bi bi-box-seam me-1"></i> Products
              </router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
              <router-link class="nav-link" to="/add-product" @click="closeNavbar">
                <i class="bi bi-plus-circle me-1"></i> Add Product
              </router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
              <router-link class="nav-link" to="/monitor" @click="closeNavbar">
                <i class="bi bi-clipboard-check me-1"></i> Orders
              </router-link>
            </li>

            <!-- CUSTOMER NAVIGATION -->
            <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
              <router-link class="nav-link" to="/products" @click="closeNavbar">
                <i class="bi bi-shop me-1"></i> Shop
              </router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
              <router-link class="nav-link position-relative" to="/cart" @click="closeNavbar">
                <i class="bi bi-cart me-1"></i> Cart
                <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
              </router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
              <router-link class="nav-link" to="/orders" @click="closeNavbar">
                <i class="bi bi-clock-history me-1"></i> Orders
              </router-link>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <!-- Show Login/Register only if LOGGED OUT -->
            <li class="nav-item" v-if="!auth.isLoggedIn">
              <router-link class="nav-link" v-if="$route.name === 'register'" to="/login" @click="closeNavbar">
                <i class="bi bi-box-arrow-in-right me-1"></i> Login
              </router-link>
              <router-link class="nav-link" v-else to="/register" @click="closeNavbar">
                <i class="bi bi-person-plus me-1"></i> Register
              </router-link>
            </li>

            <!-- Show Logout if LOGGED IN -->
            <li class="nav-item d-flex align-items-center user-nav-item" v-if="auth.isLoggedIn">
              <div class="user-info d-flex align-items-center">
                <i class="bi bi-person-circle me-1"></i>
                <span>{{ username }}</span>
              </div>
              <button class="btn btn-outline-light btn-sm ms-2" @click="logout">
                <i class="bi bi-box-arrow-right me-1"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="footer mt-auto py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-4 mb-3 mb-md-0">
            <h5 class="footer-heading">E-Store</h5>
            <p class="footer-text">Your one-stop shop for all your needs. Quality products at affordable prices.</p>
          </div>
          <div class="col-md-4 mb-3 mb-md-0">
            <h5 class="footer-heading">Quick Links</h5>
            <ul class="footer-links">
              <li><router-link to="/products">Products</router-link></li>
              <li><router-link to="/cart">Cart</router-link></li>
              <li><router-link to="/orders">Orders</router-link></li>
            </ul>
          </div>
          <div class="col-md-4">
            <h5 class="footer-heading">Contact Us</h5>
            <p class="footer-text">
              <i class="bi bi-envelope me-2"></i> support@estore.com<br>
              <i class="bi bi-telephone me-2"></i> +1 (123) 456-7890<br>
              <i class="bi bi-geo-alt me-2"></i> 123 E-Commerce St, Digital City
            </p>
          </div>
        </div>
        <div class="footer-bottom">
          <p class="mb-0">© 2025 E-Store. All rights reserved.</p>
          <div class="social-icons">
            <a href="#" class="social-icon"><i class="bi bi-facebook"></i></a>
            <a href="#" class="social-icon"><i class="bi bi-twitter"></i></a>
            <a href="#" class="social-icon"><i class="bi bi-instagram"></i></a>
          </div>
        </div>
      </div>
    </footer>
    
    <!-- Toast Notification Component -->
    <ToastNotification />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { auth } from './auth'
import axios from './axios'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'
import ToastNotification from './components/ToastNotification.vue'
import * as bootstrap from 'bootstrap'

export default {
  components: {
    ToastNotification
  },
  setup() {
    const cartCount = ref(0)
    const username = ref('')
    const navbarCollapse = ref(null)
    let bsNavbar = null
    const isNavbarOpen = ref(false)
    
    const updateCartCount = () => {
      const cart = JSON.parse(localStorage.getItem('cart')) || []
      cartCount.value = cart.length
    }
    
    const logout = () => {
      auth.logout()
      window.location.href = '/login'
    }
    
    // Toggle navbar open/close
    const toggleNavbar = () => {
      if (bsNavbar) {
        if (isNavbarOpen.value) {
          bsNavbar.hide()
        } else {
          bsNavbar.show()
        }
        isNavbarOpen.value = !isNavbarOpen.value
      }
    }
    
    // Close navbar when a link is clicked (mobile view)
    const closeNavbar = () => {
      if (bsNavbar && isNavbarOpen.value) {
        bsNavbar.hide()
        isNavbarOpen.value = false
      }
    }
    
    // Custom event bus for cart updates
    const handleStorageChange = (e) => {
      if (e.key === 'cart') {
        updateCartCount()
      }
    }
    
    // Create a custom event for cart updates
    const handleCartUpdate = () => {
      updateCartCount()
    }
    
    const fetchUsername = async () => {
      if (auth.isLoggedIn) {
        try {
          const response = await axios.get('user/')
          username.value = response.data.username
        } catch (error) {
          console.error('Failed to fetch username:', error)
        }
      }
    }
    
    onMounted(() => {
      // Check token validity on page load
      if (auth.isLoggedIn) {
        auth.checkTokenValidity()
        fetchUsername()
      }
      
      // Initialize cart count
      updateCartCount()
      
      // Listen for localStorage changes (works across tabs)
      window.addEventListener('storage', handleStorageChange)
      
      // Listen for custom cart update events
      window.addEventListener('cart-updated', handleCartUpdate)
      
      // Initialize Bootstrap navbar collapse
      const navbarElement = document.getElementById('navbarContent')
      if (navbarElement) {
        bsNavbar = new bootstrap.Collapse(navbarElement, {
          toggle: false
        })
        
        // Listen for Bootstrap events to update our state
        navbarElement.addEventListener('shown.bs.collapse', () => {
          isNavbarOpen.value = true
        })
        
        navbarElement.addEventListener('hidden.bs.collapse', () => {
          isNavbarOpen.value = false
        })
        
        // Add event listener to close navbar when clicking outside
        document.addEventListener('click', (event) => {
          if (!isNavbarOpen.value) return
          
          const isToggleButton = event.target.closest('.navbar-toggler')
          const isInsideNavbar = event.target.closest('.navbar-collapse')
          
          if (!isToggleButton && !isInsideNavbar) {
            closeNavbar()
          }
        })
      }
      
      // Close navbar when route changes
      if (window.history) {
        window.addEventListener('popstate', closeNavbar)
      }
      
      // Close navbar when window resizes to desktop size
      window.addEventListener('resize', () => {
        if (window.innerWidth >= 992 && isNavbarOpen.value) {
          closeNavbar()
        }
      })
    })
    
    onUnmounted(() => {
      window.removeEventListener('storage', handleStorageChange)
      window.removeEventListener('cart-updated', handleCartUpdate)
      window.removeEventListener('popstate', closeNavbar)
      window.removeEventListener('resize', () => {})
      
      // Remove Bootstrap event listeners
      const navbarElement = document.getElementById('navbarContent')
      if (navbarElement) {
        navbarElement.removeEventListener('shown.bs.collapse', () => {})
        navbarElement.removeEventListener('hidden.bs.collapse', () => {})
      }
      
      // Remove click event listener
      document.removeEventListener('click', () => {})
    })
    
    // Watch for changes to localStorage cart
    watch(() => localStorage.getItem('cart'), () => {
      updateCartCount()
    })
    
    return {
      auth,
      cartCount,
      username,
      logout,
      updateCartCount,
      closeNavbar,
      toggleNavbar,
      navbarCollapse
    }
  }
}
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #006884;
  --primary-dark: #053D57;
  --light: #F2F1EF;
  --accent: #97BCC7;
  --text-dark: #333333;
  --text-light: #F2F1EF;
  --border-radius: 0.5rem;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition-speed: 0.3s;
}

body {
  font-family: 'Poppins', sans-serif;
  background-color: var(--light);
  color: var(--text-dark);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background-color: var(--primary);
  box-shadow: var(--box-shadow);
  padding: 0.8rem 1rem;
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--light);
}

.nav-link {
  color: var(--light);
  font-weight: 500;
  transition: all var(--transition-speed);
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  margin: 0 0.2rem;
}

.nav-link:hover, .nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

.user-info {
  color: var(--light);
  font-weight: 500;
  opacity: 0.9;
  display: flex;
  align-items: center;
}

.user-info i {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

/* Cart Badge */
.cart-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--accent);
  color: var(--primary-dark);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background-color: var(--primary-dark);
  color: var(--light);
  padding: 2.5rem 0 1rem;
  margin-top: 2rem;
}

.footer-heading {
  font-weight: 600;
  margin-bottom: 1rem;
  color: white;
  font-size: 1.1rem;
}

.footer-text {
  opacity: 0.8;
  font-size: 0.9rem;
  line-height: 1.6;
}

.footer-links {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.5rem;
}

.footer-links a {
  color: var(--light);
  opacity: 0.8;
  text-decoration: none;
  transition: opacity var(--transition-speed);
}

.footer-links a:hover {
  opacity: 1;
  text-decoration: underline;
}

.footer-bottom {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.social-icons {
  display: flex;
  gap: 1rem;
}

.social-icon {
  color: var(--light);
  font-size: 1.2rem;
  opacity: 0.8;
  transition: opacity var(--transition-speed);
}

.social-icon:hover {
  opacity: 1;
}

/* Form styling */
.form-control {
  border-radius: var(--border-radius);
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  transition: all var(--transition-speed);
}

.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.2rem rgba(0, 104, 132, 0.25);
}

/* Button styling */
.btn {
  border-radius: var(--border-radius);
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all var(--transition-speed);
}

.btn-primary {
  background-color: var(--primary);
  border-color: var(--primary);
}

.btn-primary:hover, .btn-primary:focus {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
}

.btn-outline-primary {
  color: var(--primary);
  border-color: var(--primary);
}

.btn-outline-primary:hover {
  background-color: var(--primary);
  color: white;
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
}

/* Card styling */
.card {
  border-radius: var(--border-radius);
  border: none;
  box-shadow: var(--box-shadow);
  transition: transform var(--transition-speed);
  overflow: hidden;
}

.card:hover {
  transform: translateY(-5px);
}

.card-body {
  padding: 1.5rem;
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Navbar toggle animation */
.navbar-toggler {
  border: none;
  padding: 0.5rem;
  transition: transform 0.3s ease;
  outline: none !important;
}

.navbar-toggler:focus {
  box-shadow: none;
}

.navbar-toggler:active {
  transform: scale(0.95);
}

.navbar-toggler-icon {
  transition: transform 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 991px) {
  .navbar-collapse {
    background-color: var(--primary-dark);
    border-radius: 0 0 var(--border-radius) var(--border-radius);
    padding: 1rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    margin-top: 0.5rem;
    transition: all 0.3s ease;
  }
  
  .navbar-nav .nav-item {
    margin-bottom: 0.5rem;
  }
  
  .nav-link {
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius);
    display: block;
    width: 100%;
  }
  
  .user-nav-item {
    flex-direction: column;
    align-items: flex-start !important;
    padding: 0.75rem 0;
  }
  
  .user-info {
    margin-bottom: 0.75rem;
    width: 100%;
  }
  
  .btn-outline-light {
    width: 100%;
    text-align: left;
    padding: 0.5rem 1rem;
  }
  
  .navbar-toggler {
    border: none;
    padding: 0.5rem;
    font-size: 1.25rem;
  }
  
  .navbar-toggler:focus {
    box-shadow: none;
    outline: none;
  }
  
  .navbar-toggler-icon {
    width: 1.5em;
    height: 1.5em;
  }
  
  .cart-badge {
    top: 5px;
    right: 5px;
  }
}

@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.2rem;
  }
  
  .main-content {
    padding: 1rem 0;
  }
  
  .footer {
    padding: 2rem 0 1rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
  
  .social-icons {
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .navbar {
    padding: 0.6rem 0.75rem;
  }
  
  .nav-link {
    padding: 0.6rem 0.75rem;
  }
  
  .btn {
    padding: 0.4rem 1rem;
  }
  
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .user-info {
    font-size: 0.9rem;
  }
  
  .btn-sm {
    font-size: 0.8rem;
  }
}

/* Modal responsiveness */
.modal-dialog {
  margin: 1rem auto;
  max-width: 95%;
}

.modal-content {
  border-radius: var(--border-radius);
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.modal-header .modal-title {
  color: var(--primary-dark);
  font-weight: 600;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  background-color: white;
  border-top: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

/* Mobile modal adjustments */
@media (max-width: 576px) {
  .modal-dialog {
    margin: 0.5rem auto;
  }
  
  .modal-content {
    border-radius: calc(var(--border-radius) - 2px);
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-footer {
    padding: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .modal-footer .btn {
    flex: 1;
    min-width: 120px;
    margin: 0 !important;
  }
}

/* Confirmation modal specific styles */
.confirm-modal .modal-body {
  text-align: center;
  padding: 2rem 1.5rem;
}

.confirm-modal .modal-footer {
  justify-content: center;
}

@media (max-width: 576px) {
  .confirm-modal .modal-body {
    padding: 1.5rem 1rem;
  }
}
</style>