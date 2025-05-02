<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light px-4">
    <router-link
      class="navbar-brand"
      :to="auth.isLoggedIn ? (auth.isStaff ? '/monitor' : '/products') : '/login'"
    >
      E-Store
    </router-link>

    <div class="collapse navbar-collapse">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <!-- STAFF NAVIGATION -->
         <!-- Inside the staff section of the navbar -->
        <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
          <router-link class="nav-link" to="/monitor-products">📦 Monitor Products</router-link>
        </li>
        <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
          <router-link class="nav-link" to="/add-product">➕ Add Product</router-link>
        </li>

        <!-- CUSTOMER NAVIGATION -->
        <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
          <router-link class="nav-link" to="/products">Home</router-link>
        </li>
        <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
          <router-link class="nav-link" to="/cart">Cart</router-link>
        </li>
        <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
          <router-link class="nav-link" to="/orders">My Orders</router-link>
        </li>
      </ul>

      <ul class="navbar-nav ms-auto">
  <!-- ✅ Show Login/Register only if LOGGED OUT -->
  <li class="nav-item" v-if="!auth.isLoggedIn">
    <router-link
      class="nav-link"
      v-if="$route.name === 'register'"
      to="/login"
    >Login</router-link>
   
  </li>

  <!-- ✅ Show Logout if LOGGED IN -->
  <li class="nav-item" v-if="auth.isLoggedIn">
    <button class="btn btn-outline-danger" @click="logout">Logout</button>
  </li>
</ul>

    </div>
  </nav>

  <router-view />
</template>

<script>
import { auth } from './auth'

export default {
  setup() {
    return { auth }
  },
  methods: {
    logout() {
      const cart = localStorage.getItem('cart')
      localStorage.clear()
      localStorage.setItem('cart', cart)

      auth.isLoggedIn = false        // ✅ Reset reactivity
      auth.isStaff = false

      this.$router.push('/login')
    }
  }
}
</script>
