<template>
  <div class="container">
    <div class="admin-header mb-3 mb-md-4">
      <h2 class="section-title">
        <i class="bi bi-clipboard-check me-2"></i>Checkout Monitor
      </h2>
    </div>
    
    <!-- Stats Cards -->
    <div class="row g-3 mb-3 mb-md-4">
      <div class="col-12 col-md-4">
        <div class="stat-card card h-100">
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
      <div class="col-12 col-md-4">
        <div class="stat-card card h-100">
          <div class="card-body">
            <div class="stat-icon">
              <span>₱</span>
            </div>
            <div class="stat-info">
              <h3>₱{{ calculateTotalSales() }}</h3>
              <p>Total Sales</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="stat-card card h-100">
          <div class="card-body">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-info">
              <h3>{{ uniqueCustomers.length }}</h3>
              <p>Unique Customers</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter Panel -->
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="filter-title mb-3"><i class="bi bi-funnel me-2"></i>Search & Filter</h5>
        <div class="row g-2">
          <div class="col-12 col-md-4">
            <div class="form-group">
              <label class="form-label">Search</label>
              <div class="input-group">
                <span class="input-group-text"><i class="bi bi-search"></i></span>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  class="form-control" 
                  placeholder="Order ID..." 
                />
              </div>
            </div>
          </div>
          <div class="col-12 col-md-4">
            <div class="form-group">
              <label class="form-label">Date Range</label>
              <div class="d-flex gap-2">
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-calendar3"></i></span>
                  <input 
                    type="date" 
                    v-model="dateFrom" 
                    class="form-control" 
                    placeholder="From"
                  />
                </div>
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-calendar3"></i></span>
                  <input 
                    type="date" 
                    v-model="dateTo" 
                    class="form-control" 
                    placeholder="To"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="col-12 col-md-4">
            <div class="form-group">
              <label class="form-label">Sort By</label>
              <select v-model="sortBy" class="form-select">
                <option value="date_desc">Newest First</option>
                <option value="date_asc">Oldest First</option>
                <option value="amount_desc">Highest Amount</option>
                <option value="amount_asc">Lowest Amount</option>
              </select>
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-end mt-3">
          <button class="btn btn-outline-secondary me-2" @click="resetFilters">
            <i class="bi bi-x-circle me-1"></i>Reset
          </button>
        </div>
      </div>
    </div>

    <!-- Orders Table -->
    <div class="card mb-3 mb-md-4">
      <div class="card-header d-flex flex-column flex-md-row justify-content-between align-items-md-center">
  <h5 class="mb-2 mb-md-0">
    <i class="bi bi-list-check me-2"></i>Recent Orders
    <!-- Mobile per-page selector (visible only on mobile) -->
    <div class="mobile-pagination-select d-md-none">
      <div class="per-page-selector">
        <select v-model="perPage" class="form-select form-select-sm" aria-label="Items per page">
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
        </select>
      </div>
    </div>
  </h5>
  <!-- Desktop per-page selector (visible only on desktop) -->
  <div class="d-none d-md-flex align-items-center">
    <span class="me-2 text-muted">{{ filteredOrders.length }} orders found</span>
    <div class="per-page-selector ms-2">
      <select v-model="perPage" class="form-select form-select-sm" aria-label="Items per page">
        <option :value="5">5</option>
        <option :value="10">10</option>
        <option :value="25">25</option>
        <option :value="50">50</option>
      </select>
    </div>
  </div>
</div>
      
      <!-- Mobile View -->
      <div class="d-md-none">
        <div v-if="filteredOrders.length === 0" class="text-center py-4">
          <i class="bi bi-search text-muted" style="font-size: 2rem;"></i>
          <p class="mt-2 text-muted">No orders found</p>
        </div>
        <div v-else class="mobile-orders-list">
          <div 
            v-for="order in paginatedOrders" 
            :key="`mobile-${order.id}`" 
            class="mobile-order-item"
            @click="viewOrderDetails(order)"
          >
            <div class="d-flex justify-content-between align-items-center mb-2">
              <strong class="order-id">#{{ order.id }}</strong>
              <span class="badge bg-success">Completed</span>
            </div>
            <div class="text-muted small mb-2">{{ formatDate(order.date_ordered) }}</div>
            <div class="mb-2">{{ order.customer }}</div>
            <div class="d-flex justify-content-between">
              <span>{{ order.items ? order.items.length : 0 }} items</span>
              <strong>₱{{ calculateOrderTotal(order).toFixed(2) }}</strong>
            </div>
          </div>
          
          <!-- Mobile Pagination -->
          <div class="mobile-pagination" v-if="totalPages > 1">
            <div class="pagination-info">
              Page {{ currentPage }} of {{ totalPages }}
            </div>
            <div class="pagination-controls">
              <button 
                class="btn btn-sm btn-outline-primary" 
                :disabled="currentPage === 1"
                @click="changePage(currentPage - 1)"
              >
                <i class="bi bi-chevron-left"></i>
              </button>
              <button 
                class="btn btn-sm btn-outline-primary" 
                :disabled="currentPage === totalPages"
                @click="changePage(currentPage + 1)"
              >
                <i class="bi bi-chevron-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Desktop View -->
      <div class="table-responsive d-none d-md-block">
        <table class="table table-hover mb-0">
          <thead>
            <tr>
              <th scope="col">Order ID</th>
              <th scope="col">Date</th>
              <th scope="col">Customer</th>
              <th scope="col">Items</th>
              <th scope="col">Total</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredOrders.length === 0">
              <td colspan="7" class="text-center py-4">
                <i class="bi bi-search text-muted" style="font-size: 2rem;"></i>
                <p class="mt-2 text-muted">No orders found</p>
              </td>
            </tr>
            <tr v-for="order in paginatedOrders" :key="`desktop-${order.id}`">
              <td><span class="order-id">#{{ order.id }}</span></td>
              <td>{{ formatDate(order.date_ordered) }}</td>
              <td>{{ order.customer }}</td>
              <td>{{ order.items ? order.items.length : 0 }} items</td>
              <td>₱{{ calculateOrderTotal(order).toFixed(2) }}</td>
              <td>
                <span class="badge bg-success">Completed</span>
              </td>
              <td>
                <button class="btn btn-sm btn-primary btn-view" @click="viewOrderDetails(order)">
                  <i class="bi bi-eye"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Desktop Pagination -->
      <div class="card-footer d-none d-md-flex justify-content-between align-items-center" v-if="filteredOrders.length > 0">
        <div class="pagination-info">
          Showing {{ paginationInfo.from }} to {{ paginationInfo.to }} of {{ filteredOrders.length }} orders
        </div>
        <nav aria-label="Orders pagination">
          <ul class="pagination pagination-sm mb-0">
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

    <!-- Order Details Modal -->
    <div class="modal fade" ref="orderModal" id="orderModal" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Order Details #{{ selectedOrder?.id }}</h5>
            <button type="button" class="btn-close" @click="closeOrderModal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedOrder">
            <div class="order-info mb-4">
              <div class="row">
                <div class="col-md-6 mb-3 mb-md-0">
                  <p><strong>Customer:</strong> {{ selectedOrder.customer }}</p>
                  <p><strong>Date:</strong> {{ formatDate(selectedOrder.date_ordered) }}</p>
                </div>
                <div class="col-md-6">
                  <p><strong>Status:</strong> <span class="badge bg-success">Completed</span></p>
                  <p><strong>Total:</strong> ₱{{ calculateOrderTotal(selectedOrder).toFixed(2) }}</p>
                </div>
              </div>
            </div>
            
            <h6 class="mb-3">Order Items</h6>
            <div class="table-responsive">
              <table class="table table-bordered mb-0">
                <thead>
                  <tr>
                    <th scope="col">Product</th>
                    <th scope="col" class="text-center">Price</th>
                    <th scope="col" class="text-center">Quantity</th>
                    <th scope="col" class="text-center">Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in selectedOrder.items" :key="item.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="order-item-image me-2" v-if="getProductDetails(item.product)">
                          <img 
                            v-if="getProductDetails(item.product).image" 
                            :src="fullImageUrl(getProductDetails(item.product).image)" 
                            alt="Product"
                          />
                          <div v-else class="image-placeholder">
                            <i class="bi bi-image"></i>
                          </div>
                        </div>
                        <span>{{ getProductDetails(item.product) ? getProductDetails(item.product).name : `Product #${item.product}` }}</span>
                      </div>
                    </td>
                    <td class="text-center">₱{{ getProductDetails(item.product) ? getProductDetails(item.product).price : 'N/A' }}</td>
                    <td class="text-center">{{ item.quantity }}</td>
                    <td class="text-center">₱{{ getProductDetails(item.product) ? (getProductDetails(item.product).price * item.quantity).toFixed(2) : 'N/A' }}</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3" class="text-end"><strong>Total:</strong></td>
                    <td class="text-center">₱{{ calculateOrderTotal(selectedOrder).toFixed(2) }}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeOrderModal">Close</button>
            <button type="button" class="btn btn-primary btn-view" @click="printOrder">
              <i class="bi bi-printer me-2"></i>Print
            </button>
          </div>
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
      orders: [],
      products: [],
      selectedOrder: null,
      modalInstance: null,
      searchQuery: '',
      dateFrom: '',
      dateTo: '',
      sortBy: 'date_desc',
      currentPage: 1,
      perPage: 10,
      isFiltering: false,
      cachedOrderTotals: {}
    }
  },
  computed: {
    filteredOrders() {
      let result = [...this.orders]
      
      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(order => 
          order.id.toString().includes(query) || 
          order.customer.toString().toLowerCase().includes(query)
        )
      }
      
      // Apply date range filter
      if (this.dateFrom) {
        const fromDate = new Date(this.dateFrom)
        fromDate.setHours(0, 0, 0, 0)
        result = result.filter(order => new Date(order.date_ordered) >= fromDate)
      }
      
      if (this.dateTo) {
        const toDate = new Date(this.dateTo)
        toDate.setHours(23, 59, 59, 999)
        result = result.filter(order => new Date(order.date_ordered) <= toDate)
      }
      
      // Apply sorting
      if (this.sortBy === 'date_desc') {
        result.sort((a, b) => new Date(b.date_ordered) - new Date(a.date_ordered))
      } else if (this.sortBy === 'date_asc') {
        result.sort((a, b) => new Date(a.date_ordered) - new Date(b.date_ordered))
      } else if (this.sortBy === 'amount_desc') {
        result.sort((a, b) => this.getOrderTotal(b) - this.getOrderTotal(a))
      } else if (this.sortBy === 'amount_asc') {
        result.sort((a, b) => this.getOrderTotal(a) - this.getOrderTotal(b))
      }
      
      return result
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.filteredOrders.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredOrders.length / this.perPage)
    },
    paginationInfo() {
      const from = this.filteredOrders.length === 0 ? 0 : (this.currentPage - 1) * this.perPage + 1
      const to = Math.min(this.currentPage * this.perPage, this.filteredOrders.length)
      return { from, to }
    },
    uniqueCustomers() {
      const customerIds = new Set()
      this.orders.forEach(order => customerIds.add(order.customer))
      return Array.from(customerIds)
    }
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return ''
      return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    getProductDetails(productId) {
      return this.products.find(p => p.id === productId)
    },
    calculateOrderTotal(order) {
      let total = 0
      if (order.items) {
        order.items.forEach(item => {
          const product = this.getProductDetails(item.product)
          if (product) {
            total += product.price * item.quantity
          }
        })
      }
      return total
    },
    // Cached version for sorting performance
    getOrderTotal(order) {
      if (this.cachedOrderTotals[order.id] !== undefined) {
        return this.cachedOrderTotals[order.id]
      }
      
      const total = this.calculateOrderTotal(order)
      this.cachedOrderTotals[order.id] = total
      return total
    },
    calculateTotalSales() {
      let total = 0
      this.orders.forEach(order => {
        total += this.calculateOrderTotal(order)
      })
      return total.toFixed(2)
    },
    viewOrderDetails(order) {
      this.selectedOrder = order
      this.modalInstance = new bootstrap.Modal(this.$refs.orderModal)
      this.modalInstance.show()
    },
    closeOrderModal() {
      if (this.modalInstance) {
        this.modalInstance.hide()
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        // Scroll to top of table on page change
        this.$nextTick(() => {
          const tableElement = document.querySelector('.card')
          if (tableElement) {
            tableElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        })
      }
    },
    getPageNumbers() {
      const pages = []
      const maxVisiblePages = 5
      
      if (this.totalPages <= maxVisiblePages) {
        // Show all pages if total is less than max visible
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        // Always show first page
        pages.push(1)
        
        // Calculate start and end of visible pages
        let start = Math.max(2, this.currentPage - 1)
        let end = Math.min(this.totalPages - 1, start + 2)
        
        // Adjust start if end is at max
        if (end === this.totalPages - 1) {
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
        if (end < this.totalPages - 1) {
          pages.push('...')
        }
        
        // Always show last page
        pages.push(this.totalPages)
      }
      
      return pages
    },
    resetFilters() {
      this.searchQuery = ''
      this.dateFrom = ''
      this.dateTo = ''
      this.sortBy = 'date_desc'
      this.currentPage = 1
      this.showNotification('info', 'Filters have been reset')
    },
    applyFilters() {
      // This method is mainly for UX feedback
      this.currentPage = 1
      this.isFiltering = true
      this.showNotification('success', 'Filters applied')
      
      // Clear the cache when filters change
      this.cachedOrderTotals = {}
      
      // Force re-render of the filtered list
      this.$nextTick(() => {
        this.isFiltering = false
      })
    },
    printOrder() {
      // Create a new window for printing
      const printWindow = window.open('', '_blank', 'width=800,height=600');
      
      // Generate the HTML for the print window
      let printContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Order #${this.selectedOrder.id} - Invoice</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body {
              font-family: Arial, sans-serif;
              padding: 20px;
              color: #333;
              line-height: 1.4;
            }
            .print-container {
              max-width: 800px;
              margin: 0 auto;
              padding: 20px;
            }
            .print-header {
              text-align: center;
              margin-bottom: 30px;
              padding-bottom: 15px;
              border-bottom: 2px solid #eee;
            }
            .print-header h2 {
              margin-bottom: 5px;
              font-size: 24px;
            }
            .print-header h3 {
              margin-top: 0;
              font-size: 18px;
              color: #666;
            }
            .print-order-details {
              margin-bottom: 30px;
            }
            .print-row {
              display: flex;
              margin: 0 -15px;
            }
            .print-col {
              flex: 1;
              padding: 0 15px;
            }
            .print-items h4 {
              margin-bottom: 15px;
              font-size: 18px;
              border-bottom: 1px solid #eee;
              padding-bottom: 8px;
            }
            .print-table {
              width: 100%;
              border-collapse: collapse;
              margin-bottom: 30px;
            }
            .print-table th,
            .print-table td {
              border: 1px solid #ddd;
              padding: 8px 12px;
              text-align: left;
            }
            .print-table th {
              background-color: #f5f5f5;
            }
            .print-table tfoot {
              font-weight: bold;
            }
            .print-footer {
              margin-top: 50px;
              text-align: center;
              font-style: italic;
              color: #666;
              padding-top: 15px;
              border-top: 1px solid #eee;
            }
            @media print {
              .no-print {
                display: none;
              }
            }
            .print-button {
              background-color: #007bff;
              color: white;
              border: none;
              padding: 10px 15px;
              border-radius: 4px;
              cursor: pointer;
              margin: 20px 0;
              font-size: 14px;
            }
            .print-button:hover {
              background-color: #0069d9;
            }
          </style>
        </head>
        <body>
          <div class="print-container">
            <div class="print-header">
              <h2>Order Invoice</h2>
              <h3>Order #${this.selectedOrder.id}</h3>
            </div>
            
            <div class="print-order-details">
              <div class="print-row">
                <div class="print-col">
                  <p><strong>Customer:</strong> ${this.selectedOrder.customer}</p>
                  <p><strong>Date:</strong> ${this.formatDate(this.selectedOrder.date_ordered)}</p>
                </div>
                <div class="print-col">
                  <p><strong>Status:</strong> Completed</p>
                  <p><strong>Total:</strong> ₱${this.calculateOrderTotal(this.selectedOrder).toFixed(2)}</p>
                </div>
              </div>
            </div>
            
            <div class="print-items">
              <h4>Order Items</h4>
              <table class="print-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th style="text-align: center">Price</th>
                    <th style="text-align: center">Quantity</th>
                    <th style="text-align: center">Total</th>
                  </tr>
                </thead>
                <tbody>`;

      // Add items to the table
      this.selectedOrder.items.forEach(item => {
        const product = this.getProductDetails(item.product);
        const productName = product ? product.name : `Product #${item.product}`;
        const price = product ? product.price : 'N/A';
        const total = product ? (product.price * item.quantity).toFixed(2) : 'N/A';
        
        printContent += `
                  <tr>
                    <td>${productName}</td>
                    <td style="text-align: center">₱${price}</td>
                    <td style="text-align: center">${item.quantity}</td>
                    <td style="text-align: center">₱${total}</td>
                  </tr>`;
      });

      // Add table footer and finish the HTML
      printContent += `
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3" style="text-align: right"><strong>Total:</strong></td>
                    <td style="text-align: center">₱${this.calculateOrderTotal(this.selectedOrder).toFixed(2)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
            
            <div class="print-footer">
              <p>Thank you for your business!</p>
            </div>
            
            <div class="no-print" style="text-align: center; margin-top: 30px;">
              <button class="print-button" onclick="window.print(); window.close();">
                Print Invoice
              </button>
              <button class="print-button" style="background-color: #6c757d;" onclick="window.close();">
                Close
              </button>
            </div>
          </div>
          
          <script>
            // Auto-print on load (optional)
            window.onload = function() {
              // Uncomment the line below if you want auto-print
              // window.print();
            }
          <` + `/script>
        <` + `/body>
        <` + `/html>`;

      // Write to the new window and focus it
      printWindow.document.open();
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.focus();
    },
    async fetchOrders() {
      try {
        const res = await axios.get('orders/')
        this.orders = res.data
      } catch (err) {
        this.showNotification('error', 'Failed to load orders.')
      }
    },
    async fetchProducts() {
      try {
        const res = await axios.get('products/')
        this.products = res.data
      } catch (err) {
        this.showNotification('error', 'Failed to load products.')
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
  watch: {
    // Reset to first page when search query changes
    searchQuery() {
      this.currentPage = 1
    },
    // Reset to first page when sort order changes
    sortBy() {
      this.currentPage = 1
      // Clear the cache when sort changes
      this.cachedOrderTotals = {}
    },
    // Reset to first page when items per page changes
    perPage() {
      this.currentPage = 1
    },
    // Reset to first page when date filters change
    dateFrom() {
      this.currentPage = 1
    },
    dateTo() {
      this.currentPage = 1
    }
  },
  mounted() {
    this.fetchOrders()
    this.fetchProducts()
  }
}
</script>

<style scoped>
.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
  font-size: 1.5rem;
}

.filter-title {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.stat-card {
  border-radius: var(--border-radius);
  border: none;
  box-shadow: var(--box-shadow);
  transition: transform 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card .card-body {
  display: flex;
  align-items: center;
  padding: 1rem;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  margin-right: 1rem;
}

.stat-info h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: var(--primary-dark);
}

.stat-info p {
  margin-bottom: 0;
  color: #666;
  font-size: 0.9rem;
}

.card-header {
  background-color: var(--light);
  border-bottom: 1px solid #eee;
  padding: 1rem;
}

.card-header h5 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-dark);
  display: flex;
  align-items: center;
}

.btn-view {
  background-color: #006884;
}

.btn-view:hover {
  background-color: #f0f0f0;
  color: #006884;
}

/* Table header styling */
.table thead {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
}

.table thead th {
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-bottom: none;
  font-size: 0.9rem;
  vertical-align: middle;
  white-space: nowrap;
}

.table tbody td {
  vertical-align: middle;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.order-id {
  font-weight: 600;
  color: var(--primary-dark);
}

.order-item-image {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  flex-shrink: 0;
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
  font-size: 1.2rem;
  color: #ccc;
}

/* Search and filter panel */
.form-group {
  margin-bottom: 0.5rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
  margin-bottom: 0.25rem;
}

.input-group-text {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

/* Mobile orders list */
.mobile-orders-list {
  padding: 0.5rem;
}

.mobile-order-item {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.mobile-order-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.mobile-order-item:last-child {
  margin-bottom: 0;
}

/* Mobile pagination */
.mobile-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0.5rem;
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
}

.pagination-info {
  font-size: 0.9rem;
  color: #666;
}

.pagination-controls {
  display: flex;
  gap: 0.5rem;
}

/* Card footer with pagination */
.card-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Pagination styling */
.pagination {
  margin-bottom: 0;
}

.page-item .page-link {
  border: none;
  background-color: transparent;
  color: var(--primary);
  font-weight: 500;
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.page-item .page-link:hover {
  background-color: rgba(0, 104, 132, 0.1);
}

.page-item.active .page-link {
  background-color: var(--primary);
  color: white;
}

.page-item.disabled .page-link {
  color: #aaa;
  pointer-events: none;
}

.per-page-selector {
  display: flex;
  justify-content: flex-end;
  width: 65px;
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
  gap: 10px;
  z-index: 1000;
  transform: translateX(120%);
  transition: transform 0.3s ease;
  font-size: 0.9rem;
  max-width: 90%;
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

.notification-info {
  border-left: 4px solid #17a2b8;
}

.notification i {
  font-size: 1rem;
}

/* Modal adjustments for mobile */
.modal-dialog {
  margin: 0.5rem auto;
}

.modal-content {
  border-radius: 0.5rem;
}

.modal-header, .modal-footer {
  padding: 1rem;
}

.modal-title {
  font-size: 1.25rem;
}

/* Modal table styling */
.modal .table thead {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
}

.modal .table thead th {
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-bottom: none;
}

.modal .table tfoot {
  background-color: #f8f9fa;
  font-weight: 600;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .section-title {
    font-size: 1.3rem;
  }
  
  .filter-title {
    font-size: 1rem;
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
    font-size: 1.25rem;
  }

  .card-header h5 {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

   .mobile-pagination-select {
    margin-left: auto;
  }
  
  .per-page-selector {
    width: 60px;
  }
  
  .card-header {
    padding: 0.75rem;
  }
  
  .form-select, .form-control {
    font-size: 0.85rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-title {
    font-size: 1.1rem;
  }
  
  .btn {
    font-size: 0.85rem;
    padding: 0.375rem 0.75rem;
  }
  
  .print-row {
    flex-direction: column;
  }
  
  .print-col {
    margin-bottom: 15px;
  }
  
  /* Improve date range inputs on mobile */
  .d-flex.gap-2 {
    flex-direction: column;
    gap: 0.5rem !important;
  }
}

@media (min-width: 768px) {
  .section-title {
    font-size: 1.75rem;
  }
  
  .stat-card .card-body {
    padding: 1.25rem;
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .stat-info h3 {
    font-size: 1.8rem;
  }
  .card-header {
    padding: 1rem 1.5rem;
  }
}

/* Print styles */
@media print {
  body {
    font-size: 12pt;
    color: #000;
    background: #fff;
  }
  
  .print-table {
    font-size: 11pt;
    width: 100%;
  }
  
  .print-table th {
    background-color: #f5f5f5 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  
  .print-header h2, 
  .print-header h3 {
    color: #000 !important;
  }
  
  .print-footer {
    margin-top: 30px;
  }
}
</style>

