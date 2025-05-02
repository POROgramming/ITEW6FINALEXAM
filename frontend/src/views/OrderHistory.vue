<template>
    <div class="container mt-3">
      <h2>My Orders</h2>
      <div v-if="orders.length === 0">No orders found.</div>
      <div v-for="order in orders" :key="order.id" class="card mb-2">
        <div class="card-body">
          <h5>Order #{{ order.id }} — {{ order.date_ordered }}</h5>
          <ul>
            <li v-for="item in order.items" :key="item.id">
              {{ item.product }} — Qty: {{ item.quantity }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios'
  
  export default {
    data() {
      return { orders: [] }
    },
    async mounted() {
      const res = await axios.get('orders/')
      this.orders = res.data
    }
  }
  </script>
  