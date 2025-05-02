<template>
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>🛍️ Product Catalog</h2>
        <!-- 🔍 Search Bar -->
        <input
          v-model="searchQuery"
          type="text"
          class="form-control w-50"
          placeholder="Search products..."
        />
      </div>
  
      <div v-if="filteredProducts.length === 0">No products found.</div>
      <div v-for="product in filteredProducts" :key="product.id" class="card mb-3">
        <div class="card-body">
          <h5>{{ product.name }}</h5>
          <p>{{ product.description }}</p>
          <p>₱{{ product.price }} — Stock: {{ product.stock }}</p>
  
          <img
            v-if="product.image"
            :src="fullImageUrl(product.image)"
            class="img-fluid mb-2"
            style="max-height: 120px;"
            alt="Product"
          />
  
          <button
            class="btn btn-primary"
            @click="addToCart(product)"
            :disabled="product.stock === 0 || hasReachedLimit(product)"
          >
            {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios'
  
  export default {
    data() {
      return {
        products: [],
        cart: [], // ✅ Initialized as array
        searchQuery: ''
      }
    },
    computed: {
      filteredProducts() {
        if (!this.searchQuery) return this.products
        const q = this.searchQuery.toLowerCase()
        return this.products.filter(p =>
          p.name.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q)
        )
      }
    },
    methods: {
      fullImageUrl(path) {
        if (!path) return ''
        return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
      },
      loadCart() {
        try {
          const stored = localStorage.getItem('cart')
          this.cart = stored ? JSON.parse(stored) : []
        } catch (err) {
          console.error('❌ Error loading cart:', err)
          this.cart = []
        }
      },
      saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart))
      },
      addToCart(product) {
  if (!Array.isArray(this.cart)) {
    this.cart = []
  }

  const existing = this.cart.find(item => item.id === product.id)

  if (existing) {
    if (existing.quantity < product.stock) {
      existing.quantity += 1
    } else {
      alert(`⚠️ You can't add more than ${product.stock} items.`)
      return
    }
  } else {
    if (product.stock === 0) {
      alert('⛔ This item is out of stock.')
      return
    }
    this.cart.push({ ...product, quantity: 1 })
  }

  this.saveCart()
  alert(`${product.name} added to cart.`)
},
      hasReachedLimit(product) {
        if (!Array.isArray(this.cart)) return false
        const found = this.cart.find(item => item.id === product.id)
        return found ? found.quantity >= product.stock : false
      },
      async fetchProducts() {
        try {
          const res = await axios.get('products/')
          this.products = res.data
        } catch (err) {
          alert('❌ Failed to fetch products.')
          console.error(err)
        }
      }
    },
    mounted() {
      this.loadCart()
      this.fetchProducts()
    }
  }
  </script>
  