<template>
  <div class="container">
    <div class="admin-header mb-4">
      <h2 class="section-title">
        <i class="bi bi-box-seam me-2"></i>Product Inventory
      </h2>
      <div class="admin-actions">
        <router-link to="/add-product" class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i>Add New Product
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4">
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
      <div class="col-md-4">
        <div class="stat-card card">
          <div class="card-body">
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
      <div class="col-md-4">
        <div class="stat-card card">
          <div class="card-body">
            <div class="stat-icon">
              <i class="bi bi-cart-check"></i>
            </div>
            <div class="stat-info">
              <h3>{{ orders.length }}</h3>
              <p>Total Orders</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Table -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center flex-wrap gap-2">
        <h5 class="mb-0">Product Inventory</h5>
        <div class="search-container">
          <input 
            type="text" 
            class="form-control search-input" 
            placeholder="Search products..." 
            v-model="searchQuery"
            aria-label="Search products"
          />
          <i class="bi bi-search search-icon"></i>
        </div>
      </div>
      
      <div v-if="isLoading" class="loading-container py-5">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p>Loading products...</p>
      </div>
      
      <div v-else-if="filteredProducts.length === 0" class="empty-products py-5">
        <i class="bi bi-search-heart"></i>
        <h3>No products found</h3>
        <p>Try adjusting your search criteria.</p>
        <button class="btn btn-primary mt-3" @click="resetSearch">
          <i class="bi bi-arrow-counterclockwise me-2"></i>Reset Search
        </button>
      </div>
      
      <div v-else class="table-responsive">
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
            <tr v-for="product in paginatedProducts" :key="product.id">
              <td>
                <div class="product-image">
                  <img
                    v-if="product.image"
                    :src="fullImageUrl(product.image)"
                    :alt="product.name"
                    loading="lazy"
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
              <td>₱{{ formatPrice(product.price) }}</td>
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
                  <button class="btn btn-sm btn-primary" @click="openEditModal(product)" aria-label="Edit product">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-sm btn-danger" @click="confirmDeleteProduct(product.id)" aria-label="Delete product">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="card-footer" v-if="totalPages > 1">
        <nav aria-label="Product pagination">
          <ul class="pagination justify-content-center mb-0">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link" @click="changePage(currentPage - 1)" :disabled="currentPage === 1" aria-label="Previous page">
                <i class="bi bi-chevron-left"></i>
              </button>
            </li>
            <li
              v-for="n in getPageNumbers()"
              :key="n"
              class="page-item"
              :class="{ active: currentPage === n }"
            >
              <button v-if="n === '...'" class="page-link" disabled>{{ n }}</button>
              <button v-else class="page-link" @click="changePage(n)">{{ n }}</button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" aria-label="Next page">
                <i class="bi bi-chevron-right"></i>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Recent Orders -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">Recent Orders</h5>
      </div>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Date</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="orders.length === 0">
              <td colspan="5" class="text-center py-4">No orders found</td>
            </tr>
            <tr v-for="order in orders.slice(0, 5)" :key="order.id">
              <td>#{{ order.id }}</td>
              <td>{{ formatDate(order.date_ordered) }}</td>
              <td>{{ order.customer }}</td>
              <td>{{ order.items ? order.items.length : 0 }} items</td>
              <td>
                <span class="badge bg-success">Completed</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  <!-- Edit Modal -->
  <div class="modal fade" ref="editModal" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <form @submit.prevent="validateAndSubmitEdit" novalidate>
          <div class="modal-header">
            <h5 class="modal-title" id="editModalLabel">
              <i class="bi bi-pencil-square me-2"></i>Edit Product
            </h5>
            <button type="button" class="btn-close" @click="closeEditModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Scrollable content -->
            <div class="modal-body-scrollable">
              <!-- Product Image Preview -->
              <div class="text-center mb-4" v-if="editProduct.image">
                <div class="product-image-preview">
                  <img 
                    :src="fullImageUrl(editProduct.image)" 
                    :alt="editProduct.name" 
                    class="img-fluid rounded" 
                  />
                </div>
                <p class="image-caption mt-2">Current image</p>
              </div>
              
              <div class="form-group mb-3">
                <label class="form-label fw-medium">Product Name</label>
                <input 
                  v-model="editProduct.name" 
                  class="form-control" 
                  :class="{'is-invalid': errors.name}"
                  required 
                  @blur="validateName"
                  placeholder="Enter product name"
                />
                <div class="invalid-feedback" v-if="errors.name">{{ errors.name }}</div>
              </div>
              
              <div class="form-group mb-3">
                <label class="form-label fw-medium">Description</label>
                <textarea 
                  v-model="editProduct.description" 
                  class="form-control" 
                  :class="{'is-invalid': errors.description}"
                  rows="3" 
                  required
                  @blur="validateDescription"
                  placeholder="Enter product description"
                ></textarea>
                <div class="invalid-feedback" v-if="errors.description">{{ errors.description }}</div>
              </div>
              
              <div class="row mb-3">
                <div class="col-12 col-sm-6 mb-3 mb-sm-0">
                  <label class="form-label fw-medium">Price (₱)</label>
                  <div class="input-group">
                    <span class="input-group-text">₱</span>
                    <input 
                      type="number" 
                      v-model.number="editProduct.price" 
                      class="form-control" 
                      :class="{'is-invalid': errors.price}"
                      min="0" 
                      step="0.01" 
                      required 
                      @blur="validatePrice"
                      placeholder="0.00"
                    />
                    <div class="invalid-feedback" v-if="errors.price">{{ errors.price }}</div>
                  </div>
                </div>
                <div class="col-12 col-sm-6">
                  <label class="form-label fw-medium">Stock</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-box-seam"></i>
                    </span>
                    <input 
                      type="number" 
                      v-model.number="editProduct.stock" 
                      class="form-control" 
                      :class="{'is-invalid': errors.stock}"
                      min="0" 
                      required 
                      @blur="validateStock"
                      placeholder="0"
                    />
                    <div class="invalid-feedback" v-if="errors.stock">{{ errors.stock }}</div>
                  </div>
                </div>
              </div>
              
              <div class="form-group mb-3">
                <label class="form-label fw-medium">Product Image</label>
                <div class="custom-file-upload">
                  <input 
                    type="file" 
                    id="productImage"
                    @change="handleEditImage" 
                    class="form-control" 
                    accept="image/*" 
                  />
                  <label for="productImage" class="file-upload-label">
                    <i class="bi bi-cloud-arrow-up me-2"></i>
                    Choose a new image
                  </label>
                </div>
                <small class="text-muted d-block mt-1">
                  Recommended size: 800x800px, max 2MB
                </small>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="closeEditModal">
              <i class="bi bi-x-circle me-1"></i>Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              <i v-else class="bi bi-check-circle me-1"></i>
              {{ isSubmitting ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

<!-- Confirmation Modal -->
    <div class="modal fade confirm-modal" ref="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">Confirm Deletion</h5>
            <button type="button" class="btn-close" @click="hideConfirmModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <i class="bi bi-exclamation-triangle-fill text-danger mb-3" style="font-size: 2rem;"></i>
            <p>Are you sure you want to delete this product? This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideConfirmModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteProduct" :disabled="isDeleting">
              <span v-if="isDeleting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              <i v-else class="bi bi-trash me-1"></i>
              {{ isDeleting ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import axios from '../axios'
import * as bootstrap from 'bootstrap'
import { useToastStore } from '../stores/toastStore'

export default {
  setup() {
    const products = ref([])
    const currentPage = ref(1)
    const perPage = ref(5)
    const editProduct = reactive({ id: null, name: '', description: '', price: 0, stock: 0, image: null })
    const editImage = ref(null)
    const modalInstance = ref(null)
    const confirmModalInstance = ref(null)
    const orders = ref([])
    const searchQuery = ref('')
    const editModal = ref(null)
    const confirmModal = ref(null)
    const productToDelete = ref(null)
    const isLoading = ref(true)
    const isSubmitting = ref(false)
    const isDeleting = ref(false)
    
    const { success, error: showError } = useToastStore()
    
    // Form validation
    const errors = reactive({
      name: '',
      description: '',
      price: '',
      stock: ''
    })
    
    const validateName = () => {
      if (!editProduct.name.trim()) {
        errors.name = 'Product name is required'
        return false
      }
      errors.name = ''
      return true
    }
    
    const validateDescription = () => {
      if (!editProduct.description.trim()) {
        errors.description = 'Product description is required'
        return false
      }
      errors.description = ''
      return true
    }
    
    const validatePrice = () => {
      if (editProduct.price === null || editProduct.price === undefined) {
        errors.price = 'Price is required'
        return false
      }
      if (editProduct.price < 0) {
        errors.price = 'Price cannot be negative'
        return false
      }
      errors.price = ''
      return true
    }
    
    const validateStock = () => {
      if (editProduct.stock === null || editProduct.stock === undefined) {
        errors.stock = 'Stock quantity is required'
        return false
      }
      if (editProduct.stock < 0) {
        errors.stock = 'Stock cannot be negative'
        return false
      }
      errors.stock = ''
      return true
    }
    
    const validateForm = () => {
      const isNameValid = validateName()
      const isDescriptionValid = validateDescription()
      const isPriceValid = validatePrice()
      const isStockValid = validateStock()
      
      return isNameValid && isDescriptionValid && isPriceValid && isStockValid
    }
    
    const filteredProducts = computed(() => {
      let result = [...products.value]
      
      // Apply search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.name.toLowerCase().includes(query) || 
          p.description.toLowerCase().includes(query)
        )
      }
      
      return result
    })
    
    const totalPages = computed(() => {
      return Math.ceil(filteredProducts.value.length / perPage.value)
    })
    
    const paginatedProducts = computed(() => {
      const start = (currentPage.value - 1) * perPage.value
      return filteredProducts.value.slice(start, start + perPage.value)
    })
    
    const lowStockCount = computed(() => {
      return products.value.filter(p => p.stock < 5).length
    })
    
    const fullImageUrl = (path) => {
      if (!path) return ''
      return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
    }
    
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }
    
    const truncate = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'short', day: 'numeric' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }
    
    const getPageNumbers = () => {
      const pages = []
      const maxVisiblePages = 5
      
      if (totalPages.value <= maxVisiblePages) {
        // Show all pages if total is less than max visible
        for (let i = 1; i <= totalPages.value; i++) {
          pages.push(i)
        }
      } else {
        // Always show first page
        pages.push(1)
        
        // Calculate start and end of visible pages
        let start = Math.max(2, currentPage.value - 1)
        let end = Math.min(totalPages.value - 1, start + 2)
        
        // Adjust start if end is at max
        if (end === totalPages.value - 1) {
          start = Math.max(2, end - 2)
        }
        
        // Add ellipsis if needed
        if (start > 2) {
          pages.push('...')
        }
        
        // Add middle pages
        for (let i = start; i <= end; i++) {
          pages.push(i)
        }
        
        // Add ellipsis if needed
        if (end < totalPages.value - 1) {
          pages.push('...')
        }
        
        // Always show last page
        pages.push(totalPages.value)
      }
      
      return pages
    }
    
    const resetSearch = () => {
      searchQuery.value = ''
      currentPage.value = 1
    }
    
    const fetchProducts = async () => {
      isLoading.value = true
      try {
        const res = await axios.get('products/')
        products.value = res.data
      } catch (err) {
        showError('Failed to load products.')
        console.error(err)
      } finally {
        isLoading.value = false
      }
    }
    
    const fetchAllOrders = async () => {
      try {
        const res = await axios.get('orders/')
        orders.value = res.data
      } catch (err) {
        showError('Failed to load orders.')
        console.error(err)
      }
    }
    
    const openEditModal = (product) => {
      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })
      
      // Clone product to avoid direct mutation
      editProduct.id = product.id
      editProduct.name = product.name
      editProduct.description = product.description
      editProduct.price = product.price
      editProduct.stock = product.stock
      editProduct.image = product.image
      
      editImage.value = null
      
      if (modalInstance.value) {
        modalInstance.value.show()
      } else if (editModal.value) {
        modalInstance.value = new bootstrap.Modal(editModal.value)
        modalInstance.value.show()
      }
    }
    
    const closeEditModal = () => {
      if (modalInstance.value) {
        modalInstance.value.hide()
      }
    }
    
    const handleEditImage = (e) => {
      editImage.value = e.target.files[0]
    }
    
    const validateAndSubmitEdit = () => {
      if (validateForm()) {
        submitEdit()
      } else {
        showError('Please fix the errors in the form')
      }
    }
    
    const submitEdit = async () => {
      isSubmitting.value = true
      
      const formData = new FormData()
      formData.append('name', editProduct.name)
      formData.append('description', editProduct.description)
      formData.append('price', editProduct.price)
      formData.append('stock', editProduct.stock)
      
      if (editImage.value) {
        formData.append('image', editImage.value)
      }

      try {
        await axios.patch(`products/${editProduct.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        success('Product updated successfully!')
        fetchProducts()
        closeEditModal()
      } catch (err) {
        console.error('Error updating product:', err)
        showError('Failed to update product.')
        
        // Handle validation errors from API
        if (err.response && err.response.data) {
          const apiErrors = err.response.data
          Object.keys(apiErrors).forEach(key => {
            if (key in errors) {
              errors[key] = apiErrors[key][0]
            }
          })
        }
      } finally {
        isSubmitting.value = false
      }
    }
    
    const confirmDeleteProduct = (id) => {
      productToDelete.value = id
      if (confirmModalInstance.value) {
        confirmModalInstance.value.show()
      } else if (confirmModal.value) {
        confirmModalInstance.value = new bootstrap.Modal(confirmModal.value)
        confirmModalInstance.value.show()
      }
    }
    
    const hideConfirmModal = () => {
      if (confirmModalInstance.value) {
        confirmModalInstance.value.hide()
      }
    }
    
    const deleteProduct = async () => {
      if (!productToDelete.value) return
      
      isDeleting.value = true
      
      try {
        await axios.delete(`products/${productToDelete.value}/`)
        success('Product deleted successfully.')
        fetchProducts()
        hideConfirmModal()
      } catch (err) {
        console.error('Error deleting product:', err)
        
        if (err.response && err.response.data && err.response.data.error) {
          showError(err.response.data.error)
        } else {
          showError('Cannot delete product. It may be in an order.')
        }
      } finally {
        isDeleting.value = false
      }
    }
    
    onMounted(() => {
      // Initialize modals
      if (editModal.value) {
        modalInstance.value = new bootstrap.Modal(editModal.value)
      }
      
      if (confirmModal.value) {
        confirmModalInstance.value = new bootstrap.Modal(confirmModal.value)
      }
      
      // Check if user is staff
      const token = localStorage.getItem('access')
      const isStaff = localStorage.getItem('is_staff') === 'true'
      if (!token || !isStaff) {
        showError('Access denied. Staff only.')
        window.location.href = '/login'
        return
      }
      
      fetchProducts()
      fetchAllOrders()
    })
    
    return {
      products,
      filteredProducts,
      paginatedProducts,
      currentPage,
      totalPages,
      editProduct,
      editModal,
      confirmModal,
      orders,
      searchQuery,
      lowStockCount,
      isLoading,
      isSubmitting,
      isDeleting,
      errors,
      fullImageUrl,
      formatPrice,
      truncate,
      formatDate,
      changePage,
      getPageNumbers,
      resetSearch,
      openEditModal,
      closeEditModal,
      handleEditImage,
      validateAndSubmitEdit,
      confirmDeleteProduct,
      hideConfirmModal,
      deleteProduct,
      validateName,
      validateDescription,
      validatePrice,
      validateStock
    }
  }
}
</script>

<style scoped>
:root {
  --primary: #006884;
  --primary-dark: #053D57;
  --light: #F2F1EF;
  --accent: #97BCC7;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
  font-size: clamp(1.25rem, 2vw, 1.5rem); /* Responsive font size */
}

.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
  font-size: 0.9rem;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 104, 132, 0.3);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(1px);
}

.btn-primary:disabled {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  cursor: not-allowed;
  opacity: 0.8;
}

.stat-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
  background-color: white;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
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
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-right: 1rem;
  box-shadow: 0 4px 10px rgba(0, 104, 132, 0.2);
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
  font-size: 0.95rem;
}

.card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  background-color: white;
  margin-bottom: 2rem;
}

.card-header {
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.card-header h5 {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0;
}

.search-container {
  position: relative;
  width: 300px;
  max-width: 100%;
}

.search-input {
  width: 100%;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  padding: 0.5rem 1rem;
  padding-right: 2.5rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.25rem rgba(0, 104, 132, 0.25);
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  font-size: 1rem;
}

/* Loading animation */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.spinner {
  margin: 0 auto;
  width: 70px;
  text-align: center;
  margin-bottom: 20px;
}

.spinner > div {
  width: 18px;
  height: 18px;
  background-color: var(--primary);
  border-radius: 100%;
  display: inline-block;
  animation: sk-bouncedelay 1.4s infinite ease-in-out both;
  margin: 0 3px;
}

.spinner .bounce1 {
  animation-delay: -0.32s;
}

.spinner .bounce2 {
  animation-delay: -0.16s;
}

@keyframes sk-bouncedelay {
  0%, 80%, 100% { 
    transform: scale(0);
  } 40% { 
    transform: scale(1.0);
  }
}

.loading-container p {
  color: var(--primary-dark);
  font-weight: 500;
}

.empty-products {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-products i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--accent);
  opacity: 0.8;
}

.empty-products h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--primary-dark);
}

.empty-products p {
  color: #666;
  max-width: 300px;
  margin: 0 auto 1rem;
}

.table {
  margin-bottom: 0;
}

.table th {
  font-weight: 600;
  color: var(--primary-dark);
  border-top: none;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
}

.table td {
  vertical-align: middle;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

table thead tr th:nth-child(2) {
  width: 25rem;
}


.product-image {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
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
  margin-bottom: 0.25rem;
}

.product-description {
  font-size: 0.85rem;
  color: #666;
}

.stock-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.btn-group .btn {
  padding: 0.35rem 0.6rem;
  margin: 0 0.1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-group .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-footer {
  background-color: white;
  border-top: 1px solid #f0f0f0;
  padding: 1rem 1.5rem;
}

.pagination {
  margin-bottom: 0;
}

.page-item .page-link {
  border: none;
  background-color: #F2F1EF;
  color: #053D57;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  margin: 0 0.1rem;
  transition: all 0.2s ease;
}

.page-item .page-link:hover {
  background-color: #97BCC7;
  color: white;
}

.page-item.active .page-link {
  background-color: var(--primary);
  color: white;
  box-shadow: 0 2px 5px rgba(0, 104, 132, 0.2);
}

.page-item.disabled .page-link {
  background-color: #F2F1EF;
  color: #aaa;
}

/* Modal styling */
.modal {
  --modal-padding: 1rem;
}

.modal-content {
  border-radius: 16px;
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  padding: 1rem 1.25rem;
  flex-shrink: 0;
}

.modal-header .modal-title {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: 1.25rem;
  margin-bottom: 0;
}

.modal-body {
  padding: 0;
  overflow: hidden;
  flex: 1;
}

.modal-body-scrollable {
  padding: 1.25rem;
  overflow-y: auto;
  max-height: calc(90vh - 150px); /* Adjust based on header/footer height */
}

.modal-footer {
  background-color: white;
  border-top: 1px solid #f0f0f0;
  padding: 1rem 1.25rem;
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.modal-footer .btn {
  flex: 1;
  min-width: 120px;
}


.product-image-preview {
  max-width: 200px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.product-image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.image-caption {
  font-size: 0.85rem;
  color: #666;
}

.custom-file-upload {
  position: relative;
  overflow: hidden;
}

.custom-file-upload input[type="file"] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-upload-label {
  display: block;
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border: 1px dashed #ddd;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-upload-label:hover {
  background-color: #e9ecef;
  border-color: #ccc;
}

.form-label {
  font-weight: 500;
  color: var(--primary-dark);
  margin-bottom: 0.5rem;
}

.form-control {
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.25rem rgba(0, 104, 132, 0.25);
}

.invalid-feedback {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #dc3545;
}

.is-invalid {
  border-color: #dc3545 !important;
}

/* Enhanced Mobile Responsiveness */
@media (max-width: 992px) {
  .stat-card .card-body {
    padding: 1rem;
  }
  
  .stat-info h3 {
    font-size: 1.5rem;
  }
  
  .stat-info p {
    font-size: 0.85rem;
  }

  .modal-dialog {
    max-width: 90%;
    margin: 1rem auto;
  }
  
  .modal-body-scrollable {
    padding: 1rem;
  }
  
  .product-image-preview {
    max-width: 180px;
  }
}

@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .admin-actions {
    width: 100%;
  }
  
  .btn-primary {
    width: 100%;
    padding: 0.6rem;
  }
  
  .stat-card {
    margin-bottom: 1rem;
  }
  
  .stat-card .card-body {
    padding: 0.75rem;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
    margin-right: 0.75rem;
  }
  
  .stat-info h3 {
    font-size: 1.3rem;
  }
  
  .search-container {
    width: 100%;
    margin-top: 0.5rem;
  }
  
  .table th, .table td {
    padding: 0.5rem;
    font-size: 0.85rem;
  }
  
  .product-image {
    width: 40px;
    height: 40px;
  }
  
  .product-name {
    font-size: 0.9rem;
  }
  
  .product-description {
    display: none;
  }
  
  .stock-badge {
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .btn-group .btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.75rem;
  }
  
  .modal-dialog {
    margin: 0.5rem;
  }

  .modal-content {
    max-height: 85vh;
  }
  
  .modal-body-scrollable {
    max-height: calc(85vh - 140px);
  }
  
  
  .product-image-preview {
    max-width: 150px;
  }
  
  .form-control {
    padding: 0.6rem 0.75rem;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.2rem;
  }
  
  
  .table th {
    font-size: 0.8rem;
    padding: 0.5rem 0.3rem;
  }
  
  .table td {
    font-size: 0.8rem;
    padding: 0.5rem 0.3rem;
  }
  
  .product-image {
    width: 35px;
    height: 35px;
  }
  
  .page-item .page-link {
    padding: 0.3rem 0.5rem;
    font-size: 0.8rem;
    min-width: 30px;
  }
  
  .empty-products {
    padding: 1.5rem 1rem;
  }
  
  .empty-products i {
    font-size: 2rem;
  }
  
  .empty-products h3 {
    font-size: 1.1rem;
  }
  
  .empty-products p {
    font-size: 0.9rem;
  }

  .modal-dialog {
    max-width: 95%;
    margin: 0.5rem auto;
  }
  
  .modal-content {
    max-height: 90vh;
    border-radius: 12px;
  }
  
  .modal-body-scrollable {
    max-height: calc(90vh - 120px);
    padding: 0.75rem;
  }
  
  .modal-header {
    padding: 0.75rem;
  }
  
  .modal-title {
    font-size: 1.1rem;
  }
  
  .modal-footer {
    padding: 0.75rem;
  }
  
  .modal-footer .btn {
    min-width: 0;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    font-size: 0.85rem;
  }
  
  .product-image-preview {
    max-width: 120px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .row {
    margin-left: -0.5rem;
    margin-right: -0.5rem;
  }
  
  .row > [class^="col-"] {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .form-control {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .form-label {
    font-size: 0.9rem;
  }
}

/* Extra small devices (phones, 360px and down) */
@media (max-width: 360px) {
 
  .modal-header .modal-title {
    font-size: 1rem;
  }
  
  .btn-primary {
    font-size: 0.8rem;
  }
  
  .stat-info h3 {
    font-size: 1.1rem;
  }
  
  .stat-info p {
    font-size: 0.8rem;
  }
  
  .table th {
    font-size: 0.75rem;
  }
  
  .table td {
    font-size: 0.75rem;
  }
  
  .page-item .page-link {
    padding: 0.25rem 0.4rem;
    font-size: 0.75rem;
    min-width: 25px;
  }
  
  .modal-body-scrollable {
    padding: 0.5rem;
  }
  
  .modal-title {
    font-size: 1rem;
  }
  
  .form-control {
    padding: 0.5rem 0.6rem;
    font-size: 0.9rem;
  }
  
  .file-upload-label {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
  
  .product-image-preview {
    max-width: 100px;
  }
  
  .btn-sm {
    padding: 0.25rem 0.4rem;
    font-size: 0.75rem;
  }

  .modal-footer {
    gap: 0.25rem;
  }
  
  .modal-footer .btn {
    padding: 0.5rem;
    font-size: 0.9rem;
    min-width: 100px; /* Slightly smaller minimum width */
  }
}
/* Ensure form elements are properly sized */
.form-control {
  font-size: 1rem;
  line-height: 1.5;
}

textarea.form-control {
  min-height: 100px;
}

/* Improve input group styling */
.input-group-text {
  background-color: #f8f9fa;
  color: #495057;
}

/* Better focus states */
.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.2rem rgba(0, 104, 132, 0.25);
}

/* Button focus states */
.btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 104, 132, 0.5);
}

/* Spinner alignment */
.spinner-border {
  vertical-align: middle;
}



</style>