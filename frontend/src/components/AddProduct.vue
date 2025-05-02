<template>
    <div class="container mt-4">
      <h3>➕ Add New Product</h3>
      <form @submit.prevent="submitProduct" enctype="multipart/form-data">
        <input v-model="product.name" class="form-control mb-2" placeholder="Name" required />
        <input v-model="product.description" class="form-control mb-2" placeholder="Description" required />
        <input type="number" v-model.number="product.price" class="form-control mb-2" placeholder="Price" required />
        <input type="number" v-model.number="product.stock" class="form-control mb-2" placeholder="Stock" required />
        <input type="file" @change="handleImage" class="form-control mb-3" accept="image/*" />
        <button class="btn btn-success">Add Product</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from '../axios'
  
  export default {
    data() {
      return {
        product: { name: '', description: '', price: 0, stock: 0 },
        image: null
      }
    },
    methods: {
      handleImage(e) {
        this.image = e.target.files[0]
      },
      async submitProduct() {
        const formData = new FormData()
        for (let key in this.product) {
          formData.append(key, this.product[key])
        }
        if (this.image) formData.append('image', this.image)
  
        try {
          await axios.post('products/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('✅ Product added successfully.')
          this.$router.push('/monitor-products')
        } catch (err) {
          alert('❌ Failed to add product.')
        }
      }
    }
  }
  </script>
  