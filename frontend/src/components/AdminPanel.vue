<template>
    <div class="container mt-4">
      <h2>🛠️ Product Management</h2>
  
      <!-- Add Product Form -->
      <form @submit.prevent="addProduct" class="mb-4">
        <input v-model="newProduct.name" placeholder="Product name" class="form-control mb-2" />
        <input v-model="newProduct.description" placeholder="Description" class="form-control mb-2" />
        <input v-model.number="newProduct.price" placeholder="Price" class="form-control mb-2" />
        <input v-model.number="newProduct.stock" placeholder="Stock" class="form-control mb-2" />
        <button class="btn btn-success">Add Product</button>
      </form>
  
      <!-- Product List -->
      <div v-if="products.length === 0">No products yet.</div>
      <div v-for="product in products" :key="product.id" class="card mb-3">
        <div class="card-body">
          <h5>{{ product.name }}</h5>
          <p>{{ product.description }}</p>
          <p>₱{{ product.price }} — Stock: {{ product.stock }}</p>
          <button class="btn btn-sm btn-primary me-2" @click="editProduct(product)">Edit</button>
          <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">Delete</button>
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
        newProduct: {
          name: '',
          description: '',
          price: 0,
          stock: 0
        }
      }
    },
    methods: {
      async fetchProducts() {
        const res = await axios.get('products/')
        this.products = res.data
      },
      async addProduct() {
        await axios.post('products/', this.newProduct)
        this.newProduct = { name: '', description: '', price: 0, stock: 0 }
        this.fetchProducts()
      },
      async deleteProduct(id) {
        await axios.delete(`products/${id}/`)
        this.fetchProducts()
      },
      async editProduct(product) {
        const name = prompt('New name:', product.name)
        if (name) {
          await axios.put(`products/${product.id}/`, {
            ...product,
            name
          })
          this.fetchProducts()
        }
      }
    },
    mounted() {
      this.fetchProducts()
    }
  }
  </script>
  