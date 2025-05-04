<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <i class="bi bi-person-plus auth-icon"></i>
        <h2>Create Account</h2>
        <p>Join our community and start shopping</p>
      </div>
      
      <form @submit.prevent="validateAndRegister" class="auth-form" novalidate>
        <div class="form-group">
          <label for="username">Username</label>
          <div class="input-group" :class="{'is-invalid': errors.username}">
            <span class="input-group-text">
              <i class="bi bi-person"></i>
            </span>
            <input 
              v-model="username" 
              id="username"
              type="text" 
              class="form-control" 
              :class="{'is-invalid': errors.username}"
              placeholder="Choose a username" 
              @blur="validateUsername"
            />
          </div>
          <div class="invalid-feedback" v-if="errors.username">{{ errors.username }}</div>
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-group" :class="{'is-invalid': errors.password}">
            <span class="input-group-text">
              <i class="bi bi-key"></i>
            </span>
            <input 
              v-model="password" 
              id="password"
              :type="showPassword ? 'text' : 'password'" 
              class="form-control" 
              :class="{'is-invalid': errors.password}"
              placeholder="Create a password" 
              @blur="validatePassword"
              @input="validatePasswordStrength"
            />
            <button 
              type="button" 
              class="input-group-text password-toggle" 
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
          <div class="invalid-feedback" v-if="errors.password">{{ errors.password }}</div>
          
          <!-- Password strength meter -->
          <div class="password-strength mt-2" v-if="password">
            <div class="strength-meter">
              <div 
                class="strength-meter-fill" 
                :style="{ width: passwordStrength.score + '%' }"
                :class="passwordStrength.class"
              ></div>
            </div>
            <div class="strength-text" :class="passwordStrength.class">
              {{ passwordStrength.text }}
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <div class="input-group" :class="{'is-invalid': errors.confirmPassword}">
            <span class="input-group-text">
              <i class="bi bi-key-fill"></i>
            </span>
            <input 
              v-model="confirmPassword" 
              id="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'" 
              class="form-control" 
              :class="{'is-invalid': errors.confirmPassword}"
              placeholder="Confirm your password" 
              @blur="validateConfirmPassword"
            />
            <button 
              type="button" 
              class="input-group-text password-toggle" 
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
          <div class="invalid-feedback" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</div>
        </div>
        
        <div class="form-check mb-3">
          <input 
            class="form-check-input" 
            type="checkbox" 
            id="termsAgreed" 
            v-model="termsAgreed"
            :class="{'is-invalid': errors.termsAgreed}"
          >
          <label class="form-check-label" for="termsAgreed">
            I agree to the <a href="#" @click.prevent="showTerms">Terms and Conditions</a>
          </label>
          <div class="invalid-feedback" v-if="errors.termsAgreed">{{ errors.termsAgreed }}</div>
        </div>
        
        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
          <i v-else class="bi bi-person-plus me-2"></i>
          {{ isLoading ? 'Creating account...' : 'Create Account' }}
        </button>
        
        <div class="auth-error mt-3" v-if="error">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          {{ error }}
        </div>
      </form>
      
      <div class="auth-footer">
        <p>Already have an account? 
          <router-link to="/login" class="auth-link">Sign In</router-link>
        </p>
      </div>
    </div>
    
    <!-- Terms and Conditions Modal -->
    <div class="modal fade" ref="termsModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Terms and Conditions</h5>
            <button type="button" class="btn-close" @click="hideTerms"></button>
          </div>
          <div class="modal-body">
            <h6>1. Acceptance of Terms</h6>
            <p>By accessing and using this e-commerce platform, you agree to be bound by these Terms and Conditions.</p>
            
            <h6>2. User Accounts</h6>
            <p>You are responsible for maintaining the confidentiality of your account information and password.</p>
            
            <h6>3. Privacy Policy</h6>
            <p>Your use of our service is also governed by our Privacy Policy.</p>
            
            <h6>4. Product Information</h6>
            <p>We strive to provide accurate product information, but we do not warrant that product descriptions or other content is accurate, complete, or error-free.</p>
            
            <h6>5. Pricing and Payment</h6>
            <p>All prices are subject to change without notice. We reserve the right to refuse or cancel orders in cases of pricing errors.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideTerms">Close</button>
            <button type="button" class="btn btn-primary" @click="acceptTerms">Accept</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios'
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../stores/toastStore'
import * as bootstrap from 'bootstrap'

export default {
  name: 'UserRegister',
  setup() {
    const username = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const termsAgreed = ref(false)
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const isLoading = ref(false)
    const error = ref(null)
    const termsModal = ref(null)
    const modalInstance = ref(null)
    const router = useRouter()
    const { success, error: showError } = useToast()
    
    const errors = reactive({
      username: '',
      password: '',
      confirmPassword: '',
      termsAgreed: ''
    })
    
    const passwordStrength = computed(() => {
      if (!password.value) {
        return { score: 0, text: '', class: '' }
      }
      
      let score = 0
      let text = 'Very Weak'
      let className = 'very-weak'
      
      // Length check
      if (password.value.length >= 8) score += 20
      
      // Complexity checks
      if (/[A-Z]/.test(password.value)) score += 20 // Has uppercase
      if (/[a-z]/.test(password.value)) score += 20 // Has lowercase
      if (/[0-9]/.test(password.value)) score += 20 // Has number
      if (/[^A-Za-z0-9]/.test(password.value)) score += 20 // Has special char
      
      // Determine strength text and class
      if (score >= 80) {
        text = 'Very Strong'
        className = 'very-strong'
      } else if (score >= 60) {
        text = 'Strong'
        className = 'strong'
      } else if (score >= 40) {
        text = 'Medium'
        className = 'medium'
      } else if (score >= 20) {
        text = 'Weak'
        className = 'weak'
      }
      
      return { score, text, class: className }
    })
    
    const validateUsername = () => {
      if (!username.value.trim()) {
        errors.username = 'Username is required'
        return false
      }
      
      if (username.value.length < 3) {
        errors.username = 'Username must be at least 3 characters'
        return false
      }
      
      if (!/^[a-zA-Z0-9_]+$/.test(username.value)) {
        errors.username = 'Username can only contain letters, numbers, and underscores'
        return false
      }
      
      errors.username = ''
      return true
    }
    
    const validatePassword = () => {
      if (!password.value) {
        errors.password = 'Password is required'
        return false
      }
      
      if (password.value.length < 8) {
        errors.password = 'Password must be at least 8 characters'
        return false
      }
      
      errors.password = ''
      return true
    }
    
    const validatePasswordStrength = () => {
      // This is just to trigger the computed property
      return passwordStrength.value.score > 0
    }
    
    const validateConfirmPassword = () => {
      if (!confirmPassword.value) {
        errors.confirmPassword = 'Please confirm your password'
        return false
      }
      
      if (confirmPassword.value !== password.value) {
        errors.confirmPassword = 'Passwords do not match'
        return false
      }
      
      errors.confirmPassword = ''
      return true
    }
    
    const validateTerms = () => {
      if (!termsAgreed.value) {
        errors.termsAgreed = 'You must agree to the Terms and Conditions'
        return false
      }
      
      errors.termsAgreed = ''
      return true
    }
    
    const validateForm = () => {
      const isUsernameValid = validateUsername()
      const isPasswordValid = validatePassword()
      const isConfirmPasswordValid = validateConfirmPassword()
      const isTermsValid = validateTerms()
      
      return isUsernameValid && isPasswordValid && isConfirmPasswordValid && isTermsValid
    }
    
    const validateAndRegister = () => {
      if (validateForm()) {
        register()
      } else {
        showError('Please fix the errors in the form')
      }
    }
    
    const register = async () => {
      isLoading.value = true
      error.value = null
      
      try {
        await axios.post('register/', {
          username: username.value,
          password: password.value
        })
        
        success('Registration successful! Please log in.')
        
        // Redirect to login after a short delay
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (err) {
        console.error('Registration error:', err)
        
        if (err.response && err.response.data) {
          // Handle specific API errors
          if (err.response.data.username) {
            errors.username = err.response.data.username[0]
          }
          
          error.value = 'Registration failed. Please check the form for errors.'
        } else {
          error.value = 'Registration failed. Please try again later.'
        }
        
        showError('Registration failed. Please try again.')
      } finally {
        isLoading.value = false
      }
    }
    
    const showTerms = () => {
      if (modalInstance.value) {
        modalInstance.value.show()
      }
    }
    
    const hideTerms = () => {
      if (modalInstance.value) {
        modalInstance.value.hide()
      }
    }
    
    const acceptTerms = () => {
      termsAgreed.value = true
      errors.termsAgreed = ''
      hideTerms()
    }
    
    onMounted(() => {
      // Initialize Bootstrap modal
      if (termsModal.value) {
        modalInstance.value = new bootstrap.Modal(termsModal.value)
      }
    })
    
    return {
      username,
      password,
      confirmPassword,
      termsAgreed,
      showPassword,
      showConfirmPassword,
      isLoading,
      error,
      errors,
      passwordStrength,
      termsModal,
      validateUsername,
      validatePassword,
      validatePasswordStrength,
      validateConfirmPassword,
      validateAndRegister,
      showTerms,
      hideTerms,
      acceptTerms
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 85vh;
  padding: 2rem 1rem;
}

.auth-card {
  width: 100%;
  max-width: 500px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 2rem;
}

.auth-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.auth-header {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  color: white;
  padding: 2.5rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.auth-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
  transform: rotate(30deg);
}

.auth-icon {
  font-size: 3.5rem;
  margin-bottom: 1.25rem;
  display: inline-block;
  background: rgba(255, 255, 255, 0.15);
  width: 80px;
  height: 80px;
  line-height: 80px;
  border-radius: 50%;
  text-align: center;
}

.auth-header h2 {
  margin-bottom: 0.75rem;
  font-weight: 700;
  font-size: 1.75rem;
}

.auth-header p {
  opacity: 0.85;
  margin-bottom: 0;
  font-size: 1rem;
}

.auth-form {
  padding: 2.5rem 2rem;
}

.form-group {
  margin-bottom: 1.75rem;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #053D57;
  font-size: 0.95rem;
}

.input-group {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.input-group:focus-within {
  box-shadow: 0 3px 15px rgba(0, 104, 132, 0.15);
}

.input-group-text {
  background-color: #F2F1EF;
  border: none;
  color: #006884;
  padding: 0.75rem 1rem;
}

.form-control {
  border: none;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  background-color: #F2F1EF;
}

.form-control:focus {
  box-shadow: none;
  background-color: #F2F1EF;
}

.password-toggle {
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.password-toggle:hover {
  background-color: #97BCC7;
  color: white;
}

.password-strength {
  margin-top: 0.75rem;
}

.strength-meter {
  height: 5px;
  background-color: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.strength-meter-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.strength-meter-fill.very-weak {
  background-color: #dc3545;
}

.strength-meter-fill.weak {
  background-color: #fd7e14;
}

.strength-meter-fill.medium {
  background-color: #ffc107;
}

.strength-meter-fill.strong {
  background-color: #20c997;
}

.strength-meter-fill.very-strong {
  background-color: #28a745;
}

.strength-text {
  font-size: 0.8rem;
  text-align: right;
}

.strength-text.very-weak {
  color: #dc3545;
}

.strength-text.weak {
  color: #fd7e14;
}

.strength-text.medium {
  color: #ffc107;
}

.strength-text.strong {
  color: #20c997;
}

.strength-text.very-strong {
  color: #28a745;
}

.form-check-input:checked {
  background-color: #006884;
  border-color: #006884;
}

.form-check-label {
  font-size: 0.9rem;
  color: #666;
}

.form-check-label a {
  color: #006884;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.form-check-label a:hover {
  color: #053D57;
  text-decoration: underline;
}

.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.85rem 1.5rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 104, 132, 0.3);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(1px);
}

.btn-primary:disabled {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  cursor: not-allowed;
  opacity: 0.8;
}

.auth-error {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.auth-footer {
  padding: 1.5rem 2rem;
  text-align: center;
  border-top: 1px solid #f0f0f0;
  background-color: #fafafa;
}

.auth-link {
  color: #006884;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
  position: relative;
}

.auth-link:hover {
  color: #053D57;
}

.auth-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #053D57;
  transition: width 0.3s ease;
}

.auth-link:hover::after {
  width: 100%;
}

.invalid-feedback {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #dc3545;
}

.is-invalid {
  border-color: #dc3545 !important;
}

/* Modal styling */
.modal-content {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.modal-header {
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.modal-title {
  color: #053D57;
  font-weight: 600;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body h6 {
  color: #006884;
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.modal-body h6:first-child {
  margin-top: 0;
}

.modal-body p {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.modal-footer {
  border-top: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

/* Mobile responsiveness */
@media (max-width: 576px) {
  .auth-container {
    padding: 1rem;
  }
  
  .auth-card {
    border-radius: 12px;
  }
  
  .auth-header {
    padding: 2rem 1.5rem;
  }
  
  .auth-icon {
    font-size: 2.5rem;
    width: 60px;
    height: 60px;
    line-height: 60px;
  }
  
  .auth-header h2 {
    font-size: 1.5rem;
  }
  
  .auth-form {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  .btn-primary {
    padding: 0.75rem 1.25rem;
  }
  
  .auth-footer {
    padding: 1.25rem 1.5rem;
  }
}
</style>