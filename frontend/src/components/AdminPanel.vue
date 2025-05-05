<template>
  <div class="container">
    <div class="admin-header mb-4">
      <h2 class="section-title">
        <i class="bi bi-gear-fill me-2"></i>Admin Dashboard
      </h2>
    </div>
    
    <!-- Stats Cards for visuals-->
    <div class="row mb-4">
      <div class="col-md-4 mb-3">
        <div class="stat-card card">
          <div class="card-body">
            <div class="stat-icon">
              <i class="bi bi-box-seam"></i>
            </div>
            <div class="stat-info">
              <h3>{{ products.length }}</h3>
              <p>Total Products</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="stat-card card">
          <div class="stat-icon">
            <i class="bi bi-currency-dollar"></i>
          </div>
          <div class="stat-info">
            <h3>₱{{ calculateTotalValue() }}</h3>
            <p>Inventory Value</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="stat-card card">
          <div class="stat-icon">
            <i class="bi bi-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <h3>{{ lowStockCount }}</h3>
            <p>Low Stock Items</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Product Form -->
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0"><i class="bi bi-plus-circle me-2"></i>Add New Product</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="addProduct" class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Product Name</label>
            <input v-model="newProduct.name" placeholder="Enter product name" class="form-control" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Price (₱)</label>
            <div class="input-group">
              <span class="input-group-text">₱</span>
              <input v-model.number="newProduct.price" type="number" min="0" step="0.01" placeholder="0.00" class="form-control" required />
            </div>
          </div>
          <div class="col-md-12">
            <label class="form-label">Description</label>
            <textarea v-model="newProduct.description" placeholder="Enter product description" class="form-control" rows="3" required></textarea>
          </div>
          <div class="col-md-6">
            <label class="form-label">Stock Quantity</label>
            <input v-model.number="newProduct.stock" type="number" min="0" placeholder="0" class="form-control" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Product Image</label>
            <input type="file" @change="handleImage" class="form-control" accept="image/*" />
          </div>
          <div class="col-12">
            <button type="submit" class="btn btn-primary">
              <i class="bi bi-plus-circle me-2"></i>Add Product
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Product List -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0"><i class="bi bi-list-ul me-2"></i>Product List</h5>
        <input 
          type="text" 
          v-model="searchQuery" 
          class="form-control form-control-sm w-auto" 
          placeholder="Search products..." 
        />
      </div>
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredProducts.length === 0">
              <td colspan="5" class="text-center py-4">No products found</td>
            </tr>
            <tr v-for="product in filteredProducts" :key="product.id">
              <td>
                <div class="product-image">
                  <img
                    v-if="product.image"
                    :src="fullImageUrl(product.image)"
                    alt="Product"
                  />
                  <div v-else class="image-placeholder">
                    <i class="bi bi-image"></i>
                  </div>
                </div>
              </td>
              <td>
                <div class="product-name">{{ product.name }}</div>
                <div class="product-description">{{ truncate(product.description, 50) }}</div>
              </td>
              <td>₱{{ product.price }}</td>
              <td>
                <span 
                  class="stock-badge" 
                  :class="{
                    'bg-danger': product.stock === 0,
                    'bg-warning': product.stock > 0 && product.stock < 5,
                    'bg-success': product.stock >= 5
                  }"
                >
                  {{ product.stock }}
                </span>
              </td>
              <td>
                <div class="btn-group">
                  <button class="btn btn-sm btn-primary" @click="editProduct(product)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
      },
      selectedImage: null,
      searchQuery: ''
    }
  },
  computed: {
    filteredProducts() {
      if (!this.searchQuery) return this.products
      const query = this.searchQuery.toLowerCase()
      return this.products.filter(p => 
        p.name.toLowerCase().includes(query) || 
        p.description.toLowerCase().includes(query)
      )
    },
    lowStockCount() {
      return this.products.filter(p => p.stock < 5).length
    }
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return ''
      return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
    },
    handleImage(e) {
      this.selectedImage = e.target.files[0]
    },
    calculateTotalValue() {
      const total = this.products.reduce((sum, product) => {
        return sum + (product.price * product.stock)
      }, 0)
      return total.toFixed(2)
    },
    truncate(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    async fetchProducts() {
      try {
        const res = await axios.get('products/')
        this.products = res.data
      } catch (err) {
        this.showNotification('error', 'Failed to load products.')
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
        this.showNotification('success', 'Product added successfully!')
        this.newProduct = { name: '', description: '', price: 0, stock: 0 }
        this.selectedImage = null
        this.fetchProducts()
      } catch (err) {
        this.showNotification('error', 'Failed to add product.')
      }
    },
    async deleteProduct(id) {
      if (!confirm('Are you sure you want to delete this product?')) return
      
      try {
        await axios.delete(`products/${id}/`)
        this.showNotification('success', 'Product deleted successfully!')
        this.fetchProducts()
      } catch (err) {
        this.showNotification('error', 'Cannot delete product. It may be in an order.')
      }
    },
    async editProduct(product) {
      const name = prompt('New name:', product.name)
      if (!name) return
      
      const description = prompt('New description:', product.description)
      if (!description) return
      
      const price = prompt('New price:', product.price)
      if (!price) return
      
      const stock = prompt('New stock:', product.stock)
      if (!stock) return
      
      try {
        await axios.put(`products/${product.id}/`, {
          ...product,
          name,
          description,
          price: parseFloat(price),
          stock: parseInt(stock)
        })
        this.showNotification('success', 'Product updated successfully!')
        this.fetchProducts()
      } catch (err) {
        this.showNotification('error', 'Failed to update product.')
      }
    },
    showNotification(type, message) {
      // Create notification element
      const notification = document.createElement('div')
      notification.className = `notification notification-${type}`
      
      // Add icon based on type
      let icon = 'bi-info-circle'
      if (type === 'success') icon = 'bi-check-circle'
      if (type === 'warning') icon = 'bi-exclamation-triangle'
      if (type === 'error') icon = 'bi-x-circle'
      
      notification.innerHTML = `<i class="bi ${icon}"></i> ${message}`
      
      // Add to DOM
      document.body.appendChild(notification)
      
      // Animate in
      setTimeout(() => {
        notification.classList.add('show')
      }, 10)
      
      // Remove after delay
      setTimeout(() => {
        notification.classList.remove('show')
        setTimeout(() => {
          document.body.removeChild(notification)
        }, 300)
      }, 3000)
    }
  },
  mounted() {
    this.fetchProducts()
  }
}
</script>

<style scoped>
.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
}

.stat-card {
  border-radius: var(--border-radius);
  border: none;
  box-shadow: var(--box-shadow);
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card .card-body {
  display: flex;
  align-items: center;
  padding: 1.5rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-right: 1rem;
}

.stat-info h3 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: var(--primary-dark);
}

.stat-info p {
  margin-bottom: 0;
  color: #666;
}

.card-header {
  background-color: var(--light);
  border-bottom: 1px solid #eee;
  padding: 1rem 1.5rem;
}

.product-image {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  font-size: 1.5rem;
  color: #ccc;
}

.product-name {
  font-weight: 600;
  color: var(--primary-dark);
}

.product-description {
  font-size: 0.8rem;
  color: #666;
}

.stock-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
}

.btn-group .btn {
  padding: 0.25rem 0.5rem;
}

/* Notification system */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 5px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  transform: translateX(120%);
  transition: transform 0.3s ease;
}

.notification.show {
  transform: translateX(0);
}

.notification-success {
  border-left: 4px solid #28a745;
}

.notification-warning {
  border-left: 4px solid #ffc107;
}

.notification-error {
  border-left: 4px solid #dc3545;
}

.notification i {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .stat-card .card-body {
    padding: 1rem;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
  
  .stat-info h3 {
    font-size: 1.5rem;
  }
}
</style>