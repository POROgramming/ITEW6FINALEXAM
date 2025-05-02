<template>
    <div class="container mt-4">
      <h3>📦 Product Inventory</h3>
  
      <div v-if="paginated.length === 0">No products found.</div>
      <div v-for="product in paginated" :key="product.id" class="card mb-3">
        <div class="card-body">
          <h5>{{ product.name }}</h5>
          <p>{{ product.description }}</p>
          <p>₱{{ product.price }} — Stock: {{ product.stock }}</p>
          <img
            v-if="product.image"
            :src="fullImageUrl(product.image)"
            alt="Product image"
            class="img-thumbnail mb-2"
            style="max-height: 120px;"
          />
  
          <button class="btn btn-sm btn-primary me-2" @click="openEditModal(product)">Edit</button>
          <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">Delete</button>
        </div>
      </div>
  
      <!-- Pagination -->
      <nav v-if="totalPages > 1">
        <ul class="pagination justify-content-center mt-3">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage--">Previous</a>
          </li>
          <li
            v-for="n in totalPages"
            :key="n"
            class="page-item"
            :class="{ active: currentPage === n }"
          >
            <a class="page-link" href="#" @click.prevent="currentPage = n">{{ n }}</a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" href="#" @click.prevent="currentPage++">Next</a>
          </li>
        </ul>
      </nav>
  
      <!-- Edit Modal -->
      <div class="modal fade" ref="editModal" id="editModal">
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
                <input type="file" @change="handleEditImage" class="form-control mb-2" accept="image/*" />
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
        currentPage: 1,
        perPage: 5,
        editProduct: { id: null, name: '', description: '', price: 0, stock: 0 },
        editImage: null,
        modalInstance: null
      }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.products.length / this.perPage)
      },
      paginated() {
        const start = (this.currentPage - 1) * this.perPage
        return this.products.slice(start, start + this.perPage)
      }
    },
    methods: {
      fullImageUrl(path) {
        if (path.startsWith('http')) return path
        return `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
      },
      async fetchProducts() {
        try {
          const res = await axios.get('products/')
          this.products = res.data
        } catch {
          alert('❌ Failed to load products.')
        }
      },
      async deleteProduct(id) {
        try {
          await axios.delete(`products/${id}/`)
          alert('🗑️ Product deleted.')
          this.fetchProducts()
        } catch {
          alert('❌ Cannot delete product.')
        }
      },
      openEditModal(product) {
        this.editProduct = { ...product }
        this.editImage = null
        this.modalInstance = new bootstrap.Modal(this.$refs.editModal)
        this.modalInstance.show()
      },
      closeEditModal() {
        if (this.modalInstance) this.modalInstance.hide()
      },
      handleEditImage(e) {
        this.editImage = e.target.files[0]
      },
      async submitEdit() {
        const formData = new FormData()
        for (let key in this.editProduct) {
          if (key !== 'image') {
            formData.append(key, this.editProduct[key])
          }
        }
        if (this.editImage) {
          formData.append('image', this.editImage)
        }
  
        try {
          await axios.patch(`products/${this.editProduct.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('✅ Product updated!')
          this.fetchProducts()
          this.closeEditModal()
        } catch (err) {
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
  