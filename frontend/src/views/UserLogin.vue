<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <i class="bi bi-bag-heart-fill me-2 bag-icon"></i>
        <h2>Welcome Back</h2>
        <p>Sign in to your account to continue</p>
      </div>
      
      <form @submit.prevent="validateAndLogin" class="auth-form" novalidate>
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
              placeholder="Enter your username" 
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
              placeholder="Enter your password" 
              @blur="validatePassword"
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
        </div>
        
        <div class="form-check mb-3">
          <input class="form-check-input" type="checkbox" id="rememberMe" v-model="rememberMe">
          <label class="form-check-label" for="rememberMe">Remember me</label>
        </div>
        
        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
          <i v-else class="bi bi-box-arrow-in-right me-2"></i>
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
        
        <div class="auth-error mt-3" v-if="error">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          {{ error }}
        </div>
      </form>
      
      <div class="auth-footer">
        <p>Don't have an account? 
          <router-link to="/register" class="auth-link">Create Account</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios'
import { auth } from '../auth'
import { ref, reactive } from 'vue'
import { useToast } from '../stores/toastStore'

export default {
  name: 'UserLogin',
  setup() {
    const username = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const showPassword = ref(false)
    const isLoading = ref(false)
    const error = ref(null)
    const errors = reactive({
      username: '',
      password: ''
    })
    const { error: showError } = useToast()
    
    const validateUsername = () => {
      if (!username.value.trim()) {
        errors.username = 'Username is required'
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
      errors.password = ''
      return true
    }
    
    const validateForm = () => {
      const isUsernameValid = validateUsername()
      const isPasswordValid = validatePassword()
      return isUsernameValid && isPasswordValid
    }
    
    const validateAndLogin = () => {
      if (validateForm()) {
        login()
      } else {
        showError('Please fix the errors in the form')
      }
    }
    
    const login = async () => {
      isLoading.value = true
      error.value = null
      
      try {
        // Step 1: Get access and refresh tokens
        const res = await axios.post('token/', {
          username: username.value,
          password: password.value
        })
        localStorage.setItem('access', res.data.access)
        localStorage.setItem('refresh', res.data.refresh)
        
        if (rememberMe.value) {
          localStorage.setItem('remember_me', 'true')
        }
        
        auth.isLoggedIn = true

        // Step 2: Get user info
        const user = await axios.get('user/')
        localStorage.setItem('is_staff', user.data.is_staff)
        localStorage.setItem('user_id', user.data.id)
        localStorage.setItem('username', user.data.username)
        auth.isStaff = user.data.is_staff

        // Step 3: Redirect based on role
        window.location.href = user.data.is_staff ? '/monitor' : '/products'
      } catch (err) {
        console.error('Login error:', err)
        error.value = 'Invalid username or password. Please try again.'
        showError('Login failed: Check your username or password.')
      } finally {
        isLoading.value = false
      }
    }
    
    return {
      username,
      password,
      rememberMe,
      showPassword,
      isLoading,
      error,
      errors,
      validateUsername,
      validatePassword,
      validateAndLogin
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
  max-width: 450px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
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

.bag-icon {
  font-size: 4.5rem;
  margin-bottom: 1.25rem;
  display: inline-block;
  background: rgba(255, 255, 255, 0.15);
  width: 100px;
  height: 100px;
  line-height: 90px;
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

.form-check-input:checked {
  background-color: #006884;
  border-color: #006884;
}

.form-check-label {
  font-size: 0.9rem;
  color: #666;
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
  
  .bag-icon {
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