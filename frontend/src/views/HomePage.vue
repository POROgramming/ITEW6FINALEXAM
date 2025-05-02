<template>
    <div class="container mt-5 text-center">
      <h1 class="mb-3">Welcome to Our E-Commerce Store 🛒</h1>
      <p>Browse our products, manage your cart, or log in to get started!</p>
  
      <div class="mt-4">
        <router-link to="/products" class="btn btn-primary m-2">View Products</router-link>
        <router-link to="/login" class="btn btn-outline-secondary m-2">Login</router-link>
        <router-link to="/register" class="btn btn-outline-success m-2">Register</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  </style>
  