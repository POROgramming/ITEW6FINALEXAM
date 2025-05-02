<template>
  <div class="container mt-3">
    <h2>My Cart</h2>
    <div v-if="!cart || cart.length === 0">Cart is empty.</div>
    <ul class="list-group mb-3" v-else>
      <li
        v-for="item in cart"
        :key="item.id"
        class="list-group-item d-flex justify-content-between"
      >
        {{ item.name }} x {{ item.quantity }}
        <span>₱{{ item.price * item.quantity }}</span>
      </li>
    </ul>
    <button @click="checkout" class="btn btn-success" :disabled="!cart || cart.length === 0">
      Checkout
    </button>
  </div>
</template>

<script>
import axios from '../axios'

export default {
  data() {
    return {
      cart: []
    }
  },
  mounted() {
    const stored = localStorage.getItem('cart')
    this.cart = stored ? JSON.parse(stored) : []
  },
  methods: {
    async checkout() {
      try {
        const user = await axios.get('user/')
        const orderRes = await axios.post('orders/', {
          customer: user.data.id,
          complete: true
        })

        const orderId = orderRes.data.id
        for (const item of this.cart) {
          await axios.post('order-items/', {
            order: orderId,
            product: item.id,
            quantity: item.quantity
          })
        }

        alert('✅ Order placed successfully!')
        localStorage.removeItem('cart')
        this.cart = []
      } catch (err) {
        console.error(err)
        alert('❌ Failed to complete checkout. Please try again.')
      }
    }
  }
}
</script>
