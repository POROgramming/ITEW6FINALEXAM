<template>
    <div class="container mt-4">
      <h2>🛠️ Product Management</h2>
  
      <!-- Add Product Form -->
      <form @submit.prevent="addProduct" class="mb-4" enctype="multipart/form-data">
        <input v-model="newProduct.name" placeholder="Product name" class="form-control mb-2" required />
        <input v-model="newProduct.description" placeholder="Description" class="form-control mb-2" required />
        <input v-model.number="newProduct.price" placeholder="Price" class="form-control mb-2" required />
        <input v-model.number="newProduct.stock" placeholder="Stock" class="form-control mb-2" required />
        <input type="file" @change="handleImage" class="form-control mb-2" accept="image/*" />
        <button class="btn btn-success">Add Product</button>
      </form>
  
      <!-- Product List -->
      <div v-if="products.length === 0">No products found.</div>
      <div v-else>
        <div v-for="product in products" :key="product.id" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p>{{ product.description }}</p>
            <p>₱{{ product.price }} — Stock: {{ product.stock }}</p>
            <img
              v-if="product.image"
              :src="fullImageUrl(product.image)"
              alt="Product image"
              class="img-fluid mb-2"
              style="max-height: 150px"
            />
            <button class="btn btn-primary btn-sm me-2" @click="openEditModal(product)">Edit</button>
            <button class="btn btn-danger btn-sm" @click="deleteProduct(product.id)">Delete</button>
          </div>
        </div>
      </div>
  
      <!-- Edit Modal -->
      <div class="modal fade" tabindex="-1" ref="editModal" id="editModal">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="submitEdit">
              <div class="modal-header">
                <h5 class="modal-title">Edit Product</h5>
                <button type="button" class="btn-close" @click="closeEditModal"></button>
              </div>
              <div class="modal-body">
                <input v-model="editProduct.name" class="form-control mb-2" placeholder="Name" required />
                <input v-model="editProduct.description" class="form-control mb-2" placeholder="Description" required />
                <input type="number" v-model.number="editProduct.price" class="form-control mb-2" placeholder="Price" required />
                <input type="number" v-model.number="editProduct.stock" class="form-control mb-2" placeholder="Stock" required />
                <input type="file" @change="e => selectedEditImage = e.target.files[0]" class="form-control" />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditModal">Cancel</button>
                <button type="submit" class="btn btn-success">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios'
  import * as bootstrap from 'bootstrap'
  
  export default {
    data() {
      return {
        products: [],
        newProduct: { name: '', description: '', price: 0, stock: 0 },
        editProduct: { id: null, name: '', description: '', price: 0, stock: 0 },
        selectedImage: null,
        selectedEditImage: null,
        modalInstance: null
      }
    },
    methods: {
      fullImageUrl(path) {
        if (path.startsWith('http')) return path
        return `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
      },
      handleImage(e) {
        this.selectedImage = e.target.files[0]
      },
      async fetchProducts() {
        try {
          const res = await axios.get('products/')
          this.products = res.data
        } catch (err) {
          alert('❌ Failed to fetch products.')
        }
      },
      async addProduct() {
        const formData = new FormData()
        for (let key in this.newProduct) {
          formData.append(key, this.newProduct[key])
        }
        if (this.selectedImage) {
          formData.append('image', this.selectedImage)
        }
        try {
          await axios.post('products/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('✅ Product added!')
          this.newProduct = { name: '', description: '', price: 0, stock: 0 }
          this.selectedImage = null
          this.fetchProducts()
        } catch (err) {
          alert('❌ Failed to add product.')
        }
      },
      async deleteProduct(id) {
        try {
          await axios.delete(`products/${id}/`)
          alert('🗑️ Product deleted.')
          this.fetchProducts()
        } catch (err) {
          alert('❌ Cannot delete. Product may be in an order.')
        }
      },
      openEditModal(product) {
        this.editProduct = { ...product }
        this.selectedEditImage = null
        this.modalInstance = new bootstrap.Modal(this.$refs.editModal)
        this.modalInstance.show()
      },
      closeEditModal() {
        if (this.modalInstance) this.modalInstance.hide()
      },
      async submitEdit() {
        try {
          const formData = new FormData()
          for (let key in this.editProduct) {
            if (key !== 'image') {
              formData.append(key, this.editProduct[key])
            }
          }
          if (this.selectedEditImage) {
            formData.append('image', this.selectedEditImage)
          }
          await axios.patch(`products/${this.editProduct.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('✅ Product updated!')
          this.fetchProducts()
          this.closeEditModal()
        } catch (err) {
          console.error(err)
          alert('❌ Failed to update product.')
        }
      }
    },
    mounted() {
      const token = localStorage.getItem('access')
      const isStaff = localStorage.getItem('is_staff') === 'true'
      if (!token || !isStaff) {
        alert('⛔ Access denied. Staff only.')
        this.$router.push('/login')
        return
      }
      this.fetchProducts()
    }
  }
  </script>
  
  <style scoped>
  .modal {
    display: none;
  }
  </style>
  