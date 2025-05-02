<template>
  <div class="container mt-5">
    <h2 class="mb-3">Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" class="form-control mb-2" />
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-3" />
      <button class="btn btn-success w-100">Register</button>
    </form>
    <p class="mt-3 text-center">
      Already have an account? <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script>
import axios from '../axios'

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async register() {
      try {
        await axios.post('register/', {
          username: this.username,
          password: this.password
        })
        alert('Registration successful! Please log in.')
        this.$router.push('/login')
      } catch (err) {
        alert('Registration failed.')
      }
    }
  }
}
</script>
