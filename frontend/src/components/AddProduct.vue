<template>
  <div class="container">
    <div class="admin-header mb-3 mb-md-4">
      <h2 class="section-title">
        <i class="bi bi-plus-circle me-2"></i>Add New Product
      </h2>
      <div class="admin-actions ms-auto">
        <router-link to="/monitor-products" class="btn btn-outline-primary btn-back">
          <i class="bi bi-arrow-left me-1 me-md-2"></i>
          <span class="btn-text">Back to Products</span>
        </router-link>
      </div>
    </div>

    <div class="row">
      <div class="col-12 col-lg-8 mx-auto">
        <div class="card">
          <div class="card-body p-3 p-md-4">
            <form @submit.prevent="submitProduct" enctype="multipart/form-data">
              <div class="mb-3">
                <label class="form-label">Product Name</label>
                <input 
                  v-model="product.name" 
                  class="form-control form-control-md" 
                  placeholder="Enter product name" 
                  required 
                />
              </div>
              
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea 
                  v-model="product.description" 
                  class="form-control form-control-md" 
                  placeholder="Enter product description" 
                  rows="4"
                  required
                ></textarea>
              </div>
              
              <div class="row g-2 mb-3">
                <div class="col-12 col-md-6">
                  <label class="form-label">Price (₱)</label>
                  <div class="input-group">
                    <span class="input-group-text">₱</span>
                    <input 
                      type="number" 
                      v-model.number="product.price" 
                      class="form-control form-control-md" 
                      placeholder="0.00" 
                      min="0" 
                      step="0.01"
                      required 
                    />
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <label class="form-label">Stock Quantity</label>
                  <input 
                    type="number" 
                    v-model.number="product.stock" 
                    class="form-control form-control-md" 
                    placeholder="0" 
                    min="0"
                    required 
                  />
                </div>
              </div>
              
              <div class="mb-4">
                <label class="form-label">Product Image</label>
                <input 
                  type="file" 
                  @change="handleImage" 
                  class="form-control form-control-md" 
                  accept="image/*" 
                />
                
                <div class="image-preview mt-3" v-if="imagePreview">
                  <img :src="imagePreview" alt="Preview" class="img-thumbnail" />
                </div>
              </div>
              
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary btn-md btn-lg btn-add"
                  :disabled="isSubmitting"
                >
                  <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  <i v-else class="bi bi-plus-circle me-1 me-md-2"></i>
                  {{ isSubmitting ? 'Adding...' : 'Add Product' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//importing axios
import axios from '../axios'

export default {
  data() {
    return {
      product: { 
        name: '', 
        description: '', 
        price: 0, 
        stock: 0 
      },
      image: null,
      imagePreview: null,
      isSubmitting: false
    }
  },
  methods: {
    handleImage(e) {
      this.image = e.target.files[0]
      
      // Create preview
      if (this.image) {
        const reader = new FileReader()
        reader.onload = e => {
          this.imagePreview = e.target.result
        }
        reader.readAsDataURL(this.image)
      } else {
        this.imagePreview = null
      }
    },
    async submitProduct() {
      this.isSubmitting = true
      
      const formData = new FormData()
      for (let key in this.product) {
        formData.append(key, this.product[key])
      }
      if (this.image) formData.append('image', this.image)

      try {
        await axios.post('products/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        this.showNotification('success', 'Product added successfully!')
        
        // Reset the form
        this.product = { name: '', description: '', price: 0, stock: 0 }
        this.image = null
        this.imagePreview = null
        
        // Redirect after a short delay
        setTimeout(() => {
          this.$router.push('/monitor-products')
        }, 1500)
      } catch (err) {
        this.showNotification('error', 'Failed to add product.')
        console.error(err)
      } finally {
        this.isSubmitting = false
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
    const token = localStorage.getItem('access')
    const isStaff = localStorage.getItem('is_staff') === 'true'
    if (!token || !isStaff) {
      this.showNotification('error', 'Access denied. Staff only.')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.admin-actions {
  margin-left: auto; /* This pushes the button to the right */
}

.back-button {
  border-color: #6c757d; /* Bootstrap's secondary color */
  color: #495057; /* Dark gray color */
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: #f8f9fa; /* Light gray background on hover */
  border-color: #5a6268; /* Slightly darker border on hover */
  color: #212529; /* Darker text on hover */
}

/* Rest of your existing styles remain the same */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-title {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: 1.5rem;
  margin-bottom: 0;
}

.card {
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-label {
  font-weight: 500;
  color: var(--primary-dark);
  font-size: 0.95rem;
}

.image-preview {
  max-width: 100%;
  margin-top: 1rem;
}

.image-preview img {
  width: 100%;
  max-width: 300px;
  border-radius: 8px;
}

/* Form controls */
.form-control-md {
  padding: 0.5rem 0.75rem;
  font-size: 0.95rem;
}

.btn-md {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
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

.btn-back {
  border-color:  #053D57;
  color:  #053D57;
  transition: all 0.3s ease;
}


.btn-back:hover {
  border-color:  #006884;
  color:  #053D57;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
}

/* Notification system */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 16px;
  border-radius: 5px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  transform: translateX(120%);
  transition: transform 0.3s ease;
  font-size: 0.9rem;
  max-width: 90%;
  width: 300px;
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
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .admin-header {
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  
  .admin-actions {
    width: 100%;
  }
  
  .section-title {
    font-size: 1.3rem;
    width: 60rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .form-control-md, .btn-md {
    font-size: 0.9rem;
  }
  
  .btn-lg {
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
  }
  
  .notification {
    top: 10px;
    right: 10px;
    width: calc(100% - 20px);
    max-width: none;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.25rem;
    width: 80rem;
  }
  
  .form-label {
    font-size: 0.9rem;
  }

  .btn-lg {
    padding: 0.6rem 1rem;
  }

  .btn-back {
    padding: 0.25rem 0.5rem; /* Even more compact on very small screens */
    font-size: 0.8rem;
  }
  
  .btn-back i {
    margin-right: 0 !important; /* Remove right margin when text is hidden */
  }
  
  .form-control-md {
    padding: 0.4rem 0.6rem;
    font-size: 0.85rem;
  }
  
  textarea.form-control-md {
    min-height: 100px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1rem;
    width: 150rem;
  }
  .btn-text {
    display: none; /* Hide text on small mobile */
  }
}
</style>