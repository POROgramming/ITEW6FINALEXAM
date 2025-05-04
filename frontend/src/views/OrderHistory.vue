<template>
  <div class="container">
    <div class="order-header mb-4">
      <h2 class="section-title">
        <i class="bi bi-clock-history me-2"></i>My Orders
      </h2>
      
      <!-- Search and Sort Controls -->
      <div class="controls-wrapper mt-3">
        <div class="search-wrapper">
          <div class="input-group">
            <span class="input-group-text">
              <i class="bi bi-search"></i>
            </span>
            <input 
              type="text" 
              class="form-control" 
              v-model="searchTerm" 
              placeholder="Search orders or products..."
            />
            <button 
              v-if="searchTerm" 
              class="btn btn-outline-secondary" 
              type="button"
              @click="searchTerm = ''"
            >
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
        
        <div class="sort-wrapper">
          <div class="input-group">
            <label class="input-group-text" for="sortSelect">
              <i class="bi bi-sort-down"></i>
            </label>
            <select class="form-select" id="sortSelect" v-model="sortOption">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="highest">Highest Amount</option>
              <option value="lowest">Lowest Amount</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner">
        <div class="bounce1"></div>
        <div class="bounce2"></div>
        <div class="bounce3"></div>
      </div>
      <p class="mt-3">Loading your orders...</p>
    </div>

    <div v-else-if="orders.length === 0" class="empty-orders">
      <i class="bi bi-bag-x"></i>
      <h3>No orders found</h3>
      <p>You haven't placed any orders yet.</p>
      <router-link to="/products" class="btn btn-primary mt-3">
        <i class="bi bi-shop me-2"></i>Start Shopping
      </router-link>
    </div>

    <div v-else-if="paginatedOrders.length === 0" class="empty-orders">
      <i class="bi bi-search"></i>
      <h3>No matching orders</h3>
      <p>No orders match your search criteria.</p>
      <button class="btn btn-primary mt-3" @click="searchTerm = ''">
        <i class="bi bi-arrow-counterclockwise me-2"></i>Clear Search
      </button>
    </div>

    <div v-else>
      <!-- Results summary -->
      <div class="results-summary mb-3" v-if="searchTerm">
        <span>
          <strong>{{ filteredOrders.length }}</strong> {{ filteredOrders.length === 1 ? 'result' : 'results' }} found
          <button class="btn btn-sm btn-link p-0 ms-2" @click="searchTerm = ''">
            <i class="bi bi-x-circle"></i> Clear
          </button>
        </span>
      </div>
      
      <div class="order-card card mb-4" v-for="order in paginatedOrders" :key="order.id">
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
              <i class="bi bi-bag-check me-2"></i>Order #{{ order.id }}
            </h5>
            <span class="order-date">{{ formatDate(order.date_ordered) }}</span>
          </div>
        </div>
        <div class="card-body">
          <div class="order-items">
            <div class="order-item" v-for="item in order.items" :key="item.id">
              <div class="order-item-image" v-if="getProductDetails(item.product)">
                <img 
                  v-if="getProductDetails(item.product).image" 
                  :src="fullImageUrl(getProductDetails(item.product).image)" 
                  alt="Product"
                />
                <div v-else class="image-placeholder">
                  <i class="bi bi-image"></i>
                </div>
              </div>
              <div class="order-item-details">
                <h6 class="order-item-name">
                  {{ getProductDetails(item.product) ? getProductDetails(item.product).name : `Product #${item.product}` }}
                </h6>
                <p class="order-item-price" v-if="getProductDetails(item.product)">
                  ₱{{ getProductDetails(item.product).price }} × {{ item.quantity }}
                </p>
                <p class="order-item-quantity">
                  Quantity: {{ item.quantity }}
                </p>
                <div v-if="getProductDetails(item.product) && getProductDetails(item.product).stock === 0" class="stock-warning">
                  <i class="bi bi-exclamation-triangle-fill me-1"></i> Currently out of stock
                </div>
              </div>
              <div class="order-item-total" v-if="getProductDetails(item.product)">
                ₱{{ (getProductDetails(item.product).price * item.quantity).toFixed(2) }}
              </div>
            </div>
          </div>
          
          <div class="order-summary mt-3">
            <div class="order-total">
              <span>Total:</span>
              <span>₱{{ calculateOrderTotal(order).toFixed(2) }}</span>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
            <span class="order-status d-flex align-items-center">
              <i class="bi bi-check-circle-fill text-success me-1"></i>
              Completed
            </span>
            <button 
              class="btn btn-primary btn-sm" 
              @click="reorderItems(order)"
              :disabled="isReordering || !hasAvailableItems(order)"
            >
              <span v-if="isReordering" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-arrow-repeat me-2"></i>
              {{ isReordering ? 'Processing...' : 'Reorder' }}
            </button>
          </div>
          <div v-if="!hasAvailableItems(order)" class="reorder-warning mt-2">
            <i class="bi bi-exclamation-triangle-fill me-1"></i>
            Cannot reorder - all items are out of stock
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div class="pagination-wrapper" v-if="totalPages > 1">
        <nav aria-label="Order history pagination">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link" @click="currentPage = 1" :disabled="currentPage === 1">
                <i class="bi bi-chevron-double-left"></i>
              </button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link" @click="currentPage--" :disabled="currentPage === 1">
                <i class="bi bi-chevron-left"></i>
              </button>
            </li>
            
            <li v-for="page in displayedPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
              <button class="page-link" @click="currentPage = page">{{ page }}</button>
            </li>
            
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link" @click="currentPage++" :disabled="currentPage === totalPages">
                <i class="bi bi-chevron-right"></i>
              </button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link" @click="currentPage = totalPages" :disabled="currentPage === totalPages">
                <i class="bi bi-chevron-double-right"></i>
              </button>
            </li>
          </ul>
        </nav>
        
        <div class="items-per-page">
          <span>Items per page:</span>
          <select v-model="itemsPerPage" class="form-select form-select-sm">
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="20">20</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Confirmation Modal -->
    <div class="modal fade" ref="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">
              <i class="bi bi-cart-check me-2"></i>Confirm
            </h5>
            <button type="button" class="btn-close" @click="hideConfirmModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="confirmation-content">
              <p class="confirmation-message">{{ confirmMessage }}</p>
              
              <!-- Order Summary -->
              <div class="order-preview mt-4" v-if="orderToReorder">
                <h6 class="preview-heading">
                  <i class="bi bi-receipt me-2"></i>Order Summary
                </h6>
                <div class="preview-items">
                  <div class="preview-item" v-for="item in orderToReorder.items" :key="item.id" 
                      :class="{ 'unavailable': isItemUnavailable(item) }">
                    <div class="preview-item-details">
                      <span class="preview-item-name">
                        {{ getProductDetails(item.product) ? getProductDetails(item.product).name : `Product #${item.product}` }}
                      </span>
                      <span class="preview-item-qty">
                        × {{ item.quantity }}
                        <span v-if="isItemUnavailable(item)" class="unavailable-badge">
                          <i class="bi bi-x-circle-fill"></i> Out of stock
                        </span>
                        <span v-else-if="isItemPartiallyAvailable(item)" class="partial-badge">
                          <i class="bi bi-exclamation-circle-fill"></i> Limited stock ({{ getProductDetails(item.product).stock }})
                        </span>
                      </span>
                    </div>
                    <span class="preview-item-price" v-if="getProductDetails(item.product)">
                      ₱{{ (getProductDetails(item.product).price * (isItemUnavailable(item) ? 0 : Math.min(item.quantity, getProductDetails(item.product).stock))).toFixed(2) }}
                    </span>
                  </div>
                </div>
                
                <!-- Totals -->
                <div class="preview-total">
                  <div class="preview-total-row">
                    <span>Subtotal:</span>
                    <span>₱{{ calculateAvailableTotal(orderToReorder).subtotal.toFixed(2) }}</span>
                  </div>
                  <div class="preview-total-row grand-total">
                    <span>Total:</span>
                    <span>₱{{ calculateAvailableTotal(orderToReorder).total.toFixed(2) }}</span>
                  </div>
                </div>
                
                <!-- Validation Messages -->
                <div class="validation-section mt-3">
                  <div v-if="unavailableItems.length > 0" class="validation-message warning">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    <div>
                      <p class="validation-title">Some items are unavailable</p>
                      <p class="validation-desc">{{ unavailableItems.length }} item(s) will be skipped due to stock issues.</p>
                    </div>
                  </div>
                  
                  <div v-if="partiallyAvailableItems.length > 0" class="validation-message info">
                    <i class="bi bi-info-circle-fill me-2"></i>
                    <div>
                      <p class="validation-title">Limited stock available</p>
                      <p class="validation-desc">Some items have limited stock and quantities will be adjusted.</p>
                    </div>
                  </div>
                  
                  <div v-if="calculateAvailableTotal(orderToReorder).total === 0" class="validation-message error">
                    <i class="bi bi-x-octagon-fill me-2"></i>
                    <div>
                      <p class="validation-title">Cannot proceed</p>
                      <p class="validation-desc">All items in this order are out of stock.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="hideConfirmModal">
              <i class="bi bi-x me-1"></i>Cancel
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="confirmReorder" 
              :disabled="isReordering || (orderToReorder && calculateAvailableTotal(orderToReorder).total === 0)"
            >
              <span v-if="isReordering" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-check-circle me-2"></i>
              {{ isReordering ? 'Processing...' : 'Confirm' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios'
import { ref, computed, watch } from 'vue'
import { useToastStore } from '../stores/toastStore'
import * as bootstrap from 'bootstrap'

export default {
  setup() {
    const orders = ref([])
    const products = ref([])
    const isLoading = ref(true)
    const isReordering = ref(false)
    const confirmModal = ref(null)
    const modalInstance = ref(null)
    const confirmMessage = ref('')
    const orderToReorder = ref(null)
    const unavailableItems = ref([])
    const partiallyAvailableItems = ref([])
    const toast = useToastStore()
    
    // Search, sort, and pagination state
    const searchTerm = ref('')
    const sortOption = ref('newest')
    const currentPage = ref(1)
    const itemsPerPage = ref(5)
    
    // Reset to first page when search term or sort option changes
    watch([searchTerm, sortOption, itemsPerPage], () => {
      currentPage.value = 1
    })
    
    // Filter orders based on search term
    const filteredOrders = computed(() => {
      if (!searchTerm.value.trim()) return orders.value
      
      const term = searchTerm.value.toLowerCase().trim()
      
      return orders.value.filter(order => {
        // Search by order ID
        if (order.id.toString().includes(term)) return true
        
        // Search by product name
        if (order.items && order.items.length > 0) {
          return order.items.some(item => {
            const product = getProductDetails(item.product)
            if (product && product.name) {
              return product.name.toLowerCase().includes(term)
            }
            return false
          })
        }
        
        return false
      })
    })
    
    // Sort filtered orders
    const sortedOrders = computed(() => {
      const filtered = [...filteredOrders.value]
      
      switch (sortOption.value) {
        case 'newest':
          return filtered.sort((a, b) => new Date(b.date_ordered) - new Date(a.date_ordered))
        case 'oldest':
          return filtered.sort((a, b) => new Date(a.date_ordered) - new Date(b.date_ordered))
        case 'highest':
          return filtered.sort((a, b) => calculateOrderTotal(b) - calculateOrderTotal(a))
        case 'lowest':
          return filtered.sort((a, b) => calculateOrderTotal(a) - calculateOrderTotal(b))
        default:
          return filtered
      }
    })
    
    // Calculate total pages
    const totalPages = computed(() => {
      return Math.ceil(sortedOrders.value.length / itemsPerPage.value)
    })
    
    // Calculate which page numbers to display
    const displayedPages = computed(() => {
      const pages = []
      const maxVisiblePages = 5
      
      if (totalPages.value <= maxVisiblePages) {
        // Show all pages if there are 5 or fewer
        for (let i = 1; i <= totalPages.value; i++) {
          pages.push(i)
        }
      } else {
        // Always show first page
        pages.push(1)
        
        // Calculate middle pages
        let startPage = Math.max(2, currentPage.value - 1)
        let endPage = Math.min(totalPages.value - 1, currentPage.value + 1)
        
        // Adjust if at the beginning
        if (currentPage.value <= 3) {
          endPage = 4
        }
        
        // Adjust if at the end
        if (currentPage.value >= totalPages.value - 2) {
          startPage = totalPages.value - 3
        }
        
        // Add ellipsis after first page if needed
        if (startPage > 2) {
          pages.push('...')
        }
        
        // Add middle pages
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i)
        }
        
        // Add ellipsis before last page if needed
        if (endPage < totalPages.value - 1) {
          pages.push('...')
        }
        
        // Always show last page
        pages.push(totalPages.value)
      }
      
      return pages
    })
    
    // Get paginated orders
    const paginatedOrders = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return sortedOrders.value.slice(start, end)
    })
    
    const formatDate = (dateString) => {
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
    
    const fullImageUrl = (path) => {
      if (!path) return ''
      return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
    }
    
    const getProductDetails = (productId) => {
      return products.value.find(p => p.id === productId)
    }
    
    const calculateOrderTotal = (order) => {
      let total = 0
      if (order.items) {
        order.items.forEach(item => {
          const product = getProductDetails(item.product)
          if (product) {
            total += product.price * item.quantity
          }
        })
      }
      return total
    }
    
    const hasAvailableItems = (order) => {
      if (!order.items || order.items.length === 0) return false
      
      return order.items.some(item => {
        const product = getProductDetails(item.product)
        return product && product.stock > 0
      })
    }
    
    const getUnavailableItems = (order) => {
      if (!order.items) return []
      
      const items = []
      order.items.forEach(item => {
        const product = getProductDetails(item.product)
        if (product && product.stock === 0) {
          items.push({
            id: product.id,
            name: product.name
          })
        }
      })
      
      return items
    }
    
    const getPartiallyAvailableItems = (order) => {
      if (!order.items) return []
      
      const items = []
      order.items.forEach(item => {
        const product = getProductDetails(item.product)
        if (product && product.stock > 0 && product.stock < item.quantity) {
          items.push({
            id: product.id,
            name: product.name,
            requestedQty: item.quantity,
            availableQty: product.stock
          })
        }
      })
      
      return items
    }
    
    const isItemUnavailable = (item) => {
      const product = getProductDetails(item.product)
      return !product || product.stock === 0
    }
    
    const isItemPartiallyAvailable = (item) => {
      const product = getProductDetails(item.product)
      return product && product.stock > 0 && product.stock < item.quantity
    }
    
    const calculateAvailableTotal = (order) => {
      let subtotal = 0
      
      if (order && order.items) {
        order.items.forEach(item => {
          const product = getProductDetails(item.product)
          if (product && product.stock > 0) {
            // Only count available quantity
            const availableQty = Math.min(item.quantity, product.stock)
            subtotal += product.price * availableQty
          }
        })
      }
      
      // For now, total is same as subtotal (no tax, shipping, etc.)
      return {
        subtotal,
        total: subtotal
      }
    }
    
    const reorderItems = (order) => {
      // Check if any items are available
      if (!hasAvailableItems(order)) {
        toast.error('Cannot reorder - all items are out of stock')
        return
      }
      
      // Set the order to reorder
      orderToReorder.value = order
      
      // Get unavailable and partially available items
      unavailableItems.value = getUnavailableItems(order)
      partiallyAvailableItems.value = getPartiallyAvailableItems(order)
      
      // Set confirmation message
      if (unavailableItems.value.length > 0) {
        confirmMessage.value = 'Some items in this order are out of stock and will be skipped. Do you want to continue with the reorder?'
      } else {
        confirmMessage.value = 'Are you sure you want to reorder these items?'
      }
      
      // Show confirmation modal
      showConfirmModal()
    }
    
    const confirmReorder = async () => {
      if (!orderToReorder.value) return
      
      isReordering.value = true
      
      try {
        // Get current user
        const user = await axios.get('user/')
        
        // Create a new order
        const orderRes = await axios.post('orders/', {
          customer: user.data.id,
          complete: true
        })
        
        const newOrderId = orderRes.data.id
        let itemsAdded = 0
        
        // Add all available items from the old order to the new one
        for (const item of orderToReorder.value.items) {
          const product = getProductDetails(item.product)
          
          // Skip if product doesn't exist or is out of stock
          if (!product || product.stock < 1) continue
          
          // Determine quantity (don't exceed current stock)
          const quantity = Math.min(item.quantity, product.stock)
          
          await axios.post('order-items/', {
            order: newOrderId,
            product: item.product,
            quantity: quantity
          })
          
          itemsAdded++
        }
        
        if (itemsAdded > 0) {
          toast.success('Order placed successfully!')
          
          // Refresh orders after a short delay
          setTimeout(() => {
            fetchOrders()
          }, 1000)
        } else {
          toast.error('No items could be added to your order.')
        }
        
        hideConfirmModal()
      } catch (err) {
        console.error(err)
        toast.error('Failed to reorder. Please try again.')
      } finally {
        isReordering.value = false
      }
    }
    
    const fetchOrders = async () => {
      try {
        const res = await axios.get('orders/')
        orders.value = res.data
      } catch (err) {
        toast.error('Failed to load orders.')
        console.error(err)
      }
    }
    
    const fetchProducts = async () => {
      try {
        const res = await axios.get('products/')
        products.value = res.data
      } catch (err) {
        console.error('Failed to load products:', err)
      } finally {
        isLoading.value = false
      }
    }
    
    const showConfirmModal = () => {
      if (modalInstance.value) {
        modalInstance.value.show()
      } else if (confirmModal.value) {
        modalInstance.value = new bootstrap.Modal(confirmModal.value)
        modalInstance.value.show()
      }
    }
    
    const hideConfirmModal = () => {
      if (modalInstance.value) {
        modalInstance.value.hide()
      }
    }
    
    const init = async () => {
      try {
        // Fetch both orders and products
        await fetchOrders()
        await fetchProducts()
      } catch (err) {
        console.error(err)
        isLoading.value = false
      }
    }
    
    // Initialize
    init()
    
    return {
      orders,
      isLoading,
      isReordering,
      confirmModal,
      confirmMessage,
      orderToReorder,
      unavailableItems,
      partiallyAvailableItems,
      searchTerm,
      sortOption,
      currentPage,
      itemsPerPage,
      filteredOrders,
      sortedOrders,
      paginatedOrders,
      totalPages,
      displayedPages,
      formatDate,
      fullImageUrl,
      getProductDetails,
      calculateOrderTotal,
      hasAvailableItems,
      isItemUnavailable,
      isItemPartiallyAvailable,
      calculateAvailableTotal,
      reorderItems,
      confirmReorder,
      hideConfirmModal
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

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
  font-size: 1.5rem;
}

/* Search and Sort Controls */
.controls-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-wrapper {
  flex: 1;
  min-width: 250px;
}

.sort-wrapper {
  width: auto;
  min-width: 200px;
}

.input-group-text {
  background-color: white;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: none;
  border-color: #ced4da;
}

.form-select:focus {
  box-shadow: none;
  border-color: #ced4da;
}

/* Results summary */
.results-summary {
  font-size: 0.9rem;
  color: #666;
  padding: 0.5rem 0;
}

.results-summary .btn-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.85rem;
}

.empty-orders {
  text-align: center;
  padding: 3rem 1rem;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.empty-orders i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  color: var(--accent);
  opacity: 0.8;
}

.empty-orders h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--primary-dark);
}

.empty-orders p {
  color: #666;
  margin-bottom: 1.5rem;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.order-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
  overflow: hidden;
  margin-bottom: 1.25rem;
}

.card-header {
  background-color: var(--light);
  border-bottom: 1px solid #eee;
  padding: 1rem;
}

.card-header h5 {
  font-size: 1.1rem;
  color: var(--primary-dark);
  font-weight: 600;
}

.order-date {
  color: #666;
  font-size: 0.85rem;
}

.order-items {
  padding: 0.5rem 0;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.order-item:last-child {
  border-bottom: none;
}

.order-item-image {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  margin-right: 1rem;
}

.order-item-image img {
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

.order-item-details {
  flex: 1;
  min-width: 0;
}

.order-item-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--primary-dark);
  font-size: 0.95rem;
}

.order-item-price {
  color: #666;
  margin-bottom: 0.25rem;
  font-size: 0.85rem;
}

.order-item-quantity {
  color: #666;
  margin-bottom: 0.25rem;
  font-size: 0.85rem;
}

.stock-warning {
  color: #dc3545;
  font-size: 0.8rem;
  font-weight: 500;
}

.order-item-total {
  font-weight: 700;
  color: var(--primary);
  margin-left: 1rem;
  font-size: 0.95rem;
  min-width: 60px;
  text-align: right;
}

.order-summary {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.order-total {
  display: flex;
  justify-content: space-between;
  font-weight: 700;
  color: var(--primary-dark);
  font-size: 1rem;
}

.card-footer {
  background-color: white;
  border-top: 1px solid #eee;
  padding: 1rem;
}

.order-status {
  font-weight: 500;
  color: #28a745;
  font-size: 0.9rem;
}

.reorder-warning {
  color: #dc3545;
  font-size: 0.85rem;
  text-align: right;
}

.card-footer .btn {
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.pagination {
  margin-bottom: 0;
}

.page-item.active .page-link {
  background-color: var(--primary);
  border-color: var(--primary);
}

.page-link {
  color: var(--primary);
  border-radius: 6px;
  margin: 0 0.15rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0;
}

.page-link:focus {
  box-shadow: none;
}

.page-link:hover {
  background-color: #f8f9fa;
  color: var(--primary-dark);
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #666;
}

.items-per-page .form-select {
  width: auto;
  padding: 0.25rem 1.5rem 0.25rem 0.5rem;
  font-size: 0.85rem;
}

.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 104, 132, 0.3);
}

.btn-primary:disabled {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  cursor: not-allowed;
  opacity: 0.8;
}

/* Loading animation */
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

/* Modal styling */
.modal-content {
  border-radius: 16px;
  border: none;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #eaeaea;
  padding: 1.25rem 1.5rem;
}

.modal-header .modal-title {
  color: var(--primary-dark);
  font-weight: 700;
  font-size: 1.15rem;
  display: flex;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #eaeaea;
}

.confirmation-message {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0;
}

/* Order Preview */
.order-preview {
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 1.25rem;
  background-color: #f9f9fb;
  margin-top: 1.5rem;
}

.preview-heading {
  font-weight: 600;
  color: var(--primary-dark);
  font-size: 0.95rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.preview-items {
  max-height: 250px;
  overflow-y: auto;
  margin-bottom: 1rem;
  padding-right: 0.5rem;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eaeaea;
}

.preview-item:last-child {
  border-bottom: none;
}

.preview-item.unavailable {
  opacity: 0.65;
}

.preview-item-details {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.preview-item-name {
  font-weight: 500;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.preview-item-qty {
  font-size: 0.8rem;
  color: #666;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preview-item-price {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--primary);
  margin-left: 1rem;
}

.unavailable-badge {
  font-size: 0.75rem;
  color: #dc3545;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background-color: rgba(220, 53, 69, 0.1);
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
}

.partial-badge {
  font-size: 0.75rem;
  color: #fd7e14;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background-color: rgba(253, 126, 20, 0.1);
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
}

/* Totals */
.preview-total {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed #ddd;
}

.preview-total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.preview-total-row.grand-total {
  font-weight: 700;
  color: var(--primary-dark);
  font-size: 1rem;
  margin-top: 0.5rem;
}

/* Validation Messages */
.validation-section {
  margin-top: 1.25rem;
}

.validation-message {
  display: flex;
  align-items: flex-start;
  padding: 0.85rem;
  border-radius: 10px;
  margin-bottom: 0.75rem;
}

.validation-message:last-child {
  margin-bottom: 0;
}

.validation-message.warning {
  background-color: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
}

.validation-message.warning i {
  color: #ffc107;
}

.validation-message.info {
  background-color: rgba(13, 110, 253, 0.1);
  border-left: 3px solid #0d6efd;
}

.validation-message.info i {
  color: #0d6efd;
}

.validation-message.error {
  background-color: rgba(220, 53, 69, 0.1);
  border-left: 3px solid #dc3545;
}

.validation-message.error i {
  color: #dc3545;
}

.validation-message i {
  font-size: 1.1rem;
  margin-right: 0.75rem;
  margin-top: 0.1rem;
}

.validation-title {
  font-weight: 600;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.validation-desc {
  font-size: 0.8rem;
  margin-bottom: 0;
  color: #555;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 104, 132, 0.3);
}

.btn-outline-secondary {
  border: 1px solid #ced4da;
  background: transparent;
  color: #495057;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #333;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .controls-wrapper {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .search-wrapper,
  .sort-wrapper {
    width: 100%;
  }
  
  .modal-dialog {
    margin: 0.5rem;
  }
  
  .modal-header .modal-title {
    font-size: 1.05rem;
  }
  
  .modal-body {
    padding: 1.25rem;
  }
  
  .confirmation-message {
    font-size: 0.95rem;
  }
  
  .preview-heading {
    font-size: 0.9rem;
  }
  
  .preview-item {
    padding: 0.6rem 0;
  }
  
  .preview-item-name {
    font-size: 0.85rem;
  }
  
  .preview-item-qty {
    font-size: 0.75rem;
  }
  
  .preview-item-price {
    font-size: 0.85rem;
  }
  
  .validation-title {
    font-size: 0.8rem;
  }
  
  .validation-desc {
    font-size: 0.75rem;
  }
  
  .pagination-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.3rem;
  }
  
  .empty-orders i {
    font-size: 2.5rem;
  }
  
  .empty-orders h3 {
    font-size: 1.2rem;
  }
  
  .order-card {
    margin-bottom: 1rem;
  }
  
  .card-header h5 {
    font-size: 1rem;
  }
  
  .order-date {
    font-size: 0.8rem;
  }
  
  .order-item {
    padding: 0.5rem 0;
    position: relative;
  }
  
  .order-item-image {
    width: 50px;
    height: 50px;
    margin-right: 0.75rem;
  }
  
  .order-item-name {
    font-size: 0.9rem;
  }
  
  .order-item-price,
  .order-item-quantity {
    font-size: 0.8rem;
  }
  
  .order-item-total {
    position: absolute;
    right: 0;
    bottom: 0.5rem;
    margin-left: 0;
    font-size: 0.9rem;
  }
  
  .order-total {
    font-size: 0.95rem;
  }
  
  .order-status {
    font-size: 0.85rem;
  }
  
  .card-footer .btn {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.2rem;
  }
  
  .empty-orders {
    padding: 1.5rem 0.5rem;
  }
  
  .empty-orders i {
    font-size: 2rem;
  }
  
  .empty-orders h3 {
    font-size: 1.1rem;
  }
  
  .empty-orders p {
    font-size: 0.9rem;
  }
  
  .empty-orders .btn {
    width: 100%;
  }
  
  .order-item-image {
    width: 45px;
    height: 45px;
  }
  
  .order-item-name {
    font-size: 0.85rem;
  }
  
  .order-item-price,
  .order-item-quantity {
    font-size: 0.75rem;
  }
  
  .order-item-total {
    font-size: 0.85rem;
  }
  
  .card-footer {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .card-footer .btn {
    width: 100%;
  }
  
  .modal-header {
    padding: 1rem 1.25rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-footer {
    padding: 1rem 1.25rem;
    flex-direction: column;
    gap: 0.75rem;
    height: auto;
  }
  
  .btn-primary, 
  .btn-outline-secondary {
    width: 100%;
    padding: 0.65rem 1rem;
    font-size: 0.9rem;
  }
  
  .page-link {
    min-width: 32px;
    height: 32px;
    font-size: 0.85rem;
  }
  .items-per-page .form-select{
    padding-right: 1.5rem;
    padding-left: 0.7rem;
  }
}
</style>



