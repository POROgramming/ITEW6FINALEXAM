<template>
  <div class="container mt-5">
    <h2 class="mb-4">Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" class="form-control mb-2" />
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-3" />
      <button class="btn btn-primary w-100">Login</button>
    </form>
    <p class="mt-3 text-center">
      Don't have an account? <router-link to="/register">Register here</router-link>
    </p>
  </div>
</template>

<script>
import axios from '../axios'
import { auth } from '../auth'

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        // Step 1: Get access and refresh tokens
        const res = await axios.post('token/', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('access', res.data.access)
        localStorage.setItem('refresh', res.data.refresh)
        auth.isLoggedIn = true

        // Step 2: Get user info
        const user = await axios.get('user/')
        localStorage.setItem('is_staff', user.data.is_staff)
        auth.isStaff = user.data.is_staff

        // Step 3: Redirect based on role
        this.$router.push(user.data.is_staff ? '/monitor' : '/products')

      } catch (err) {
        alert('Login failed: Check your username or password.')
      }
    }
  }
}
</script>
