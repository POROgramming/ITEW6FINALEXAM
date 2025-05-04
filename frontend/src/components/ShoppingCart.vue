<template>
  <div class="container">
    <div class="cart-header mb-4">
      <h2 class="section-title">
        <i class="bi bi-cart me-2"></i>Shopping Cart
      </h2>
    </div>

    <div v-if="!cart || cart.length === 0" class="empty-cart">
      <div class="empty-cart-content">
        <i class="bi bi-cart-x"></i>
        <h3>Your cart is empty</h3>
        <p>Add some products to your cart to continue shopping.</p>
        <router-link to="/products" class="btn btn-primary mt-3">
          <i class="bi bi-shop me-2"></i>Continue Shopping
        </router-link>
      </div>
    </div>

    <div v-else class="row">
      <div class="col-lg-8">
        <div class="cart-items card mb-4">
          <div class="card-header">
            <h5 class="mb-0">Cart Items ({{ cart.length }})</h5>
          </div>
          <div class="card-body p-0">
            <div class="cart-item" v-for="(item, index) in cart" :key="index">
              <div class="cart-item-image">
                <img
                  v-if="item && item.product && item.product.image"
                  :src="fullImageUrl(item.product.image)"
                  :alt="item.product ? item.product.name : 'Product'"
                  loading="lazy"
                />
                <div v-else class="image-placeholder">
                  <i class="bi bi-image"></i>
                </div>
              </div>
              <div class="cart-item-details">
                <h5 class="cart-item-name">{{ item && item.product ? item.product.name : 'Unknown Product' }}</h5>
                <p class="cart-item-description">
                  {{ item && item.product ? truncate(item.product.description, 100) : 'No description available' }}
                </p>
                <div class="cart-item-price">₱{{ formatPrice(item && item.product ? item.product.price : 0) }}</div>
                <div v-if="item && item.product && item.product.stock === 0" class="stock-warning">
                  <i class="bi bi-exclamation-triangle-fill me-1"></i> Out of stock
                </div>
              </div>
              <div class="cart-item-quantity">
                <div class="quantity-selector">
                  <button 
                    class="btn btn-sm btn-outline-secondary" 
                    @click="decrementQuantity(index)"
                    :disabled="!item || item.quantity <= 1 || (item.product && item.product.stock === 0)"
                    aria-label="Decrease quantity"
                  >
                    <i class="bi bi-dash"></i>
                  </button>
                  <input 
                    type="number" 
                    class="form-control form-control-sm" 
                    v-model.number="item.quantity" 
                    min="1" 
                    :max="item && item.product ? item.product.stock : 1"
                    :disabled="item && item.product && item.product.stock === 0"
                    @change="validateQuantity(index, item && item.product ? item.product.stock : 1)"
                    aria-label="Quantity"
                  />
                  <button 
                    class="btn btn-sm btn-outline-secondary" 
                    @click="incrementQuantity(index, item && item.product ? item.product.stock : 1)"
                    :disabled="!item || !item.product || item.quantity >= item.product.stock || item.product.stock === 0"
                    aria-label="Increase quantity"
                  >
                    <i class="bi bi-plus"></i>
                  </button>
                </div>
              </div>
              <div class="cart-item-total">
                ₱{{ formatPrice(item && item.product ? (item.product.price * item.quantity) : 0) }}
              </div>
              <div class="cart-item-actions">
                <button class="btn btn-sm btn-danger" @click="removeItem(index)" aria-label="Remove item">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <div class="d-flex justify-content-between flex-wrap gap-2">
              <button class="btn btn-outline-danger" @click="confirmClearCart">
                <i class="bi bi-trash me-2"></i>Clear Cart
              </button>
              <router-link to="/products" class="btn btn-outline-primary">
                <i class="bi bi-shop me-2"></i>Continue Shopping
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="cart-summary card">
          <div class="card-header">
            <h5 class="mb-0">Order Summary</h5>
          </div>
          <div class="card-body">
            <div class="summary-item">
              <span>Subtotal</span>
              <span>₱{{ formatPrice(calculateSubtotal()) }}</span>
            </div>
            <div class="summary-item">
              <span>Shipping</span>
              <span>₱{{ formatPrice(shippingCost) }}</span>
            </div>
            <div class="summary-item">
              <span>Tax (12%)</span>
              <span>₱{{ formatPrice(calculateTax()) }}</span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-total">
              <span>Total</span>
              <span>₱{{ formatPrice(calculateTotal()) }}</span>
            </div>
            
            <!-- Promo code section -->
            <div class="promo-section mt-3">
              <div class="input-group" :class="{'is-invalid': promoError}">
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="Promo code" 
                  v-model="promoCode"
                  :class="{'is-invalid': promoError}"
                  aria-label="Promo code"
                />
                <button 
                  class="btn btn-outline-primary" 
                  type="button" 
                  @click="applyPromoCode"
                  :disabled="isApplyingPromo || !promoCode"
                >
                  <span v-if="isApplyingPromo" class="spinner-border spinner-border-sm" role="status"></span>
                  <span v-else>Apply</span>
                </button>
              </div>
              <div class="invalid-feedback" v-if="promoError">{{ promoError }}</div>
              <div class="promo-success" v-if="activePromo">
                <i class="bi bi-check-circle-fill me-1"></i>
                {{ activePromo.code }} applied: {{ activePromo.discount }}% off
              </div>
            </div>
          </div>
          <div class="card-footer">
            <button 
              class="btn btn-primary w-100" 
              @click="proceedToCheckout" 
              :disabled="isCheckingOut || hasOutOfStockItems || cart.length === 0"
            >
              <span v-if="isCheckingOut" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-credit-card me-2"></i>
              {{ isCheckingOut ? 'Processing...' : 'Proceed to Checkout' }}
            </button>
            <div class="checkout-warning mt-2" v-if="hasOutOfStockItems">
              <i class="bi bi-exclamation-triangle-fill me-1"></i>
              Please remove out of stock items before checkout
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Confirmation Modal -->
    <div class="modal fade confirm-modal" ref="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">Confirm Action</h5>
            <button type="button" class="btn-close" @click="hideConfirmModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <i class="bi bi-question-circle-fill text-warning mb-3" style="font-size: 2rem;"></i>
            <p class="mb-0">{{ confirmMessage }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideConfirmModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmAction">Confirm</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../axios'
import { useToast } from '../stores/toastStore'
import * as bootstrap from 'bootstrap'

export default {
  setup() {
    const cart = ref([])
    const shippingCost = ref(50.00)
    const router = useRouter()
    const { success, warning, error, info } = useToast()
    const latestProducts = ref([])
    const isCheckingOut = ref(false)
    const promoCode = ref('')
    const promoError = ref('')
    const isApplyingPromo = ref(false)
    const activePromo = ref(null)
    
    // Confirmation modal
    const confirmModal = ref(null)
    const modalInstance = ref(null)
    const confirmMessage = ref('')
    const confirmCallback = ref(null)
    
    // Check if cart has out of stock items
    const hasOutOfStockItems = computed(() => {
      return cart.value.some(item => 
        item && item.product && item.product.stock === 0
      )
    })
    
    // Notify other components about cart updates
    const notifyCartUpdate = () => {
      // Dispatch a custom event that App.vue listens for
      window.dispatchEvent(new CustomEvent('cart-updated'))
    }
    
    const fullImageUrl = (path) => {
      if (!path) return ''
      return path.startsWith('http')
        ? path
        : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
    }
    
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }
    
    const truncate = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    const calculateSubtotal = () => {
      let subtotal = cart.value.reduce((total, item) => {
        if (!item || !item.product || item.product.stock === 0) return total
        return total + (item.product.price * item.quantity)
      }, 0)
      
      // Apply promo discount if active
      if (activePromo.value) {
        subtotal = subtotal * (1 - activePromo.value.discount / 100)
      }
      
      return subtotal
    }
    
    const calculateTax = () => {
      return calculateSubtotal() * 0.12
    }
    
    const calculateTotal = () => {
      return calculateSubtotal() + calculateTax() + shippingCost.value
    }
    
    const incrementQuantity = (index, maxStock) => {
      try {
        if (index < 0 || index >= cart.value.length) return
        
        const item = cart.value[index]
        if (!item || !item.product || item.product.stock === 0) return
        
        if (item.quantity < maxStock) {
          item.quantity++
          updateCart()
          info('Quantity updated')
        }
      } catch (err) {
        console.error('Error incrementing quantity:', err)
        error('Failed to update quantity')
      }
    }
    
    const decrementQuantity = (index) => {
      try {
        if (index < 0 || index >= cart.value.length) return
        
        const item = cart.value[index]
        if (!item || item.product.stock === 0) return
        
        if (item.quantity > 1) {
          item.quantity--
          updateCart()
          info('Quantity updated')
        }
      } catch (err) {
        console.error('Error decrementing quantity:', err)
        error('Failed to update quantity')
      }
    }
    
    const validateQuantity = (index, maxStock) => {
      try {
        if (index < 0 || index >= cart.value.length) return
        
        const item = cart.value[index]
        if (!item) return
        
        if (item.product && item.product.stock === 0) {
          item.quantity = 0
          warning(`${item.product.name} is out of stock`)
          updateCart()
          return
        }
        
        if (item.quantity < 1) {
          item.quantity = 1
          updateCart()
        } else if (item.quantity > maxStock) {
          item.quantity = maxStock
          warning(`Maximum stock available: ${maxStock}`)
          updateCart()
        }
      } catch (err) {
        console.error('Error validating quantity:', err)
        error('Failed to update quantity')
      }
    }
    
    const removeItem = (index) => {
      confirmMessage.value = 'Are you sure you want to remove this item from your cart?'
      confirmCallback.value = () => {
        try {
          if (index < 0 || index >= cart.value.length) return
          
          const productName = cart.value[index]?.product?.name || 'Item'
          cart.value.splice(index, 1)
          updateCart()
          success(`Removed ${productName} from cart`)
          hideConfirmModal()
        } catch (err) {
          console.error('Error removing item:', err)
          error('Failed to remove item')
        }
      }
      showConfirmModal()
    }
    
    const clearCart = () => {
      try {
        cart.value = []
        updateCart()
        activePromo.value = null
        promoCode.value = ''
        promoError.value = ''
        info('Cart cleared')
        hideConfirmModal()
      } catch (err) {
        console.error('Error clearing cart:', err)
        error('Failed to clear cart')
      }
    }
    
    const confirmClearCart = () => {
      confirmMessage.value = 'Are you sure you want to clear your cart? This will remove all items.'
      confirmCallback.value = clearCart
      showConfirmModal()
    }
    
    const updateCart = () => {
      try {
        localStorage.setItem('cart', JSON.stringify(cart.value))
        // Trigger storage event for other components to detect
        window.dispatchEvent(new Event('storage'))
        // Notify about cart update
        notifyCartUpdate()
      } catch (err) {
        console.error('Error updating cart:', err)
        error('Failed to update cart')
      }
    }
    
    // Mock promo codes for demonstration
    const promoCodes = [
      { code: 'WELCOME10', discount: 10 },
      { code: 'SAVE20', discount: 20 },
      { code: 'SPECIAL30', discount: 30 }
    ]
    
    const applyPromoCode = () => {
      if (!promoCode.value) {
        promoError.value = 'Please enter a promo code'
        return
      }
      
      isApplyingPromo.value = true
      promoError.value = ''
      
      // Simulate API call with timeout
      setTimeout(() => {
        const foundPromo = promoCodes.find(p => p.code === promoCode.value.toUpperCase())
        
        if (foundPromo) {
          activePromo.value = foundPromo
          success(`Promo code ${foundPromo.code} applied successfully!`)
        } else {
          promoError.value = 'Invalid promo code'
          error('Invalid promo code. Please try again.')
        }
        
        isApplyingPromo.value = false
      }, 800)
    }
    
    const proceedToCheckout = async () => {
      if (hasOutOfStockItems.value) {
        error('Please remove out of stock items before checkout')
        return
      }
      
      if (!validateCart()) {
        return
      }
      
      isCheckingOut.value = true
      
      try {
        if (!cart.value.length) {
          error('Your cart is empty')
          return
        }
        
        // Validate cart items
        for (const item of cart.value) {
          if (!item || !item.product || !item.product.id) {
            error('Invalid item in cart. Please remove it and try again.')
            return
          }
          
          // Skip items with 0 stock
          if (item.product.stock === 0) {
            error(`${item.product.name} is out of stock. Please remove it from your cart.`)
            return
          }
        }
        
        // Get current user
        const userRes = await axios.get('user/')
        
        // Create order
        const orderRes = await axios.post('orders/', {
          customer: userRes.data.id,
          complete: true
        })
        
        const orderId = orderRes.data.id
        
        // Add order items
        for (const item of cart.value) {
          // Skip items with 0 stock
          if (item.product.stock === 0) continue
          
          await axios.post('order-items/', {
            order: orderId,
            product: item.product.id,
            quantity: item.quantity
          })
        }
        
        // Clear cart after successful checkout
        cart.value = []
        updateCart()
        activePromo.value = null
        promoCode.value = ''
        
        success('Order placed successfully!')
        
        // Redirect to orders page
        setTimeout(() => {
          router.push('/orders')
        }, 1500)
      } catch (err) {
        console.error('Error during checkout:', err)
        error('Failed to place order. Please try again.')
      } finally {
        isCheckingOut.value = false
      }
    }
    
    const validateCart = () => {
      if (!cart.value.length) {
        error('Your cart is empty')
        return false
      }
      
      let isValid = true
      
      // Check for invalid items
      cart.value.forEach((item) => {
        if (!item || !item.product || !item.product.id) {
          error('Invalid item in cart. Please remove it and try again.')
          isValid = false
          return
        }
        
        // Check if product is out of stock
        if (item.product.stock === 0) {
          warning(`${item.product.name} is out of stock. Please remove it from your cart.`)
          isValid = false
          return
        }
        
        // Check if quantity exceeds stock
        if (item.quantity > item.product.stock) {
          warning(`Quantity for ${item.product.name} exceeds available stock. Adjusting to maximum.`)
          item.quantity = item.product.stock
          updateCart()
        }
      })
      
      return isValid
    }
    
    // Fetch latest product data
    const fetchLatestProducts = async () => {
      try {
        const res = await axios.get('products/')
        latestProducts.value = res.data
        
        // Update cart items with latest product data
        updateCartWithLatestData()
      } catch (err) {
        console.error('Error fetching products:', err)
      }
    }
    
    // Update cart items with latest product data
    const updateCartWithLatestData = () => {
      if (!cart.value.length || !latestProducts.value.length) return
      
      let cartUpdated = false
      
      cart.value.forEach(item => {
        if (!item || !item.product || !item.product.id) return
        
        // Find the latest product data
        const latestProduct = latestProducts.value.find(p => p.id === item.product.id)
        
        if (latestProduct) {
          // Check if product data needs updating
          if (
            item.product.name !== latestProduct.name ||
            item.product.price !== latestProduct.price ||
            item.product.image !== latestProduct.image ||
            item.product.description !== latestProduct.description ||
            item.product.stock !== latestProduct.stock
          ) {
            // Update product data while preserving quantity
            const quantity = item.quantity
            item.product = {
              id: latestProduct.id,
              name: latestProduct.name,
              price: latestProduct.price,
              description: latestProduct.description,
              image: latestProduct.image,
              stock: latestProduct.stock
            }
            item.quantity = quantity
            
            // Ensure quantity doesn't exceed current stock
            if (item.quantity > latestProduct.stock) {
              item.quantity = latestProduct.stock > 0 ? latestProduct.stock : 0
              warning(`Quantity for ${latestProduct.name} adjusted to match available stock`)
            }
            
            cartUpdated = true
          }
        }
      })
      
      // Save updated cart if changes were made
      if (cartUpdated) {
        updateCart()
        info('Cart updated with latest product information')
      }
    }
    
    const loadCart = () => {
      try {
        // Load cart from localStorage
        const savedCart = localStorage.getItem('cart')
        if (savedCart) {
          const parsedCart = JSON.parse(savedCart)
          
          // Validate cart items
          cart.value = parsedCart.filter(item => {
            return item && item.product && item.product.id
          })
          
          // If invalid items were filtered out, update localStorage
          if (cart.value.length !== parsedCart.length) {
            updateCart()
            warning('Some invalid items were removed from your cart')
          }
        }
      } catch (err) {
        console.error('Error loading cart:', err)
        error('Failed to load cart')
        cart.value = []
      }
    }
    
    // Modal functions
    const showConfirmModal = () => {
      if (modalInstance.value) {
        modalInstance.value.show()
      }
    }
    
    const hideConfirmModal = () => {
      if (modalInstance.value) {
        modalInstance.value.hide()
      }
    }
    
    const confirmAction = () => {
      if (typeof confirmCallback.value === 'function') {
        confirmCallback.value()
      }
    }
    
    // Poll for product updates every minute
    let productUpdateInterval
    
    onMounted(() => {
      loadCart()
      fetchLatestProducts()
      
      // Initialize modal
      if (confirmModal.value) {
        modalInstance.value = new bootstrap.Modal(confirmModal.value)
      }
      
      // Set up polling for product updates
      productUpdateInterval = setInterval(() => {
        fetchLatestProducts()
      }, 60000) // Check every minute
      
      // Notify about initial cart state
      notifyCartUpdate()
    })
    
    onUnmounted(() => {
      if (productUpdateInterval) {
        clearInterval(productUpdateInterval)
      }
    })
    
    // Watch for changes in cart to validate
    watch(cart, () => {
      validateCart()
    }, { deep: true })
    
    return {
      cart,
      shippingCost,
      fullImageUrl,
      formatPrice,
      truncate,
      calculateSubtotal,
      calculateTax,
      calculateTotal,
      incrementQuantity,
      decrementQuantity,
      validateQuantity,
      removeItem,
      clearCart,
      confirmClearCart,
      updateCart,
      proceedToCheckout,
      isCheckingOut,
      promoCode,
      promoError,
      isApplyingPromo,
      activePromo,
      applyPromoCode,
      confirmModal,
      confirmMessage,
      hideConfirmModal,
      confirmAction,
      hasOutOfStockItems
    }
  }
}
</script>

<style scoped>
/* Base font sizes for desktop */
:root {
  --primary: #006884;
  --primary-dark: #053D57;
  --light: #F2F1EF;
  --accent: #97BCC7;
  
  /* Font size variables */
  --font-xs: 0.75rem;   /* 12px */
  --font-sm: 0.875rem;  /* 14px */
  --font-base: 1rem;    /* 16px */
  --font-md: 1.125rem;  /* 18px */
  --font-lg: 1.25rem;   /* 20px */
  --font-xl: 1.5rem;    /* 24px */
  --font-2xl: 1.75rem;  /* 28px */
  --font-3xl: 2rem;     /* 32px */
}

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
  font-size: var(--font-2xl);
}

.empty-cart {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.empty-cart-content {
  text-align: center;
  padding: 2rem;
}

.empty-cart i {
  font-size: var(--font-3xl);
  margin-bottom: 1.5rem;
  color: var(--accent);
  opacity: 0.8;
}

.empty-cart h3 {
  font-size: var(--font-xl);
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--primary-dark);
}

.empty-cart p {
  color: #666;
  margin-bottom: 1.5rem;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
  font-size: var(--font-base);
}

.cart-items {
  border-radius: 16px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.card-header {
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.card-header h5 {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: var(--font-lg);
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  position: relative;
  transition: background-color 0.2s ease;
}

.cart-item:hover {
  background-color: #f9f9f9;
}

.cart-item:last-child {
  border-bottom: none;
}

.cart-item-image {
  width: 90px;
  height: 90px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  margin-right: 1.25rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.cart-item-image img {
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
  font-size: var(--font-2xl);
  color: #ccc;
}

.cart-item-details {
  flex: 1;
  min-width: 0;
  margin-right: 1.5rem;
}

.cart-item-name {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--primary-dark);
  font-size: var(--font-md);
}

.cart-item-description {
  color: #666;
  margin-bottom: 0.75rem;
  font-size: var(--font-sm);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cart-item-price {
  font-weight: 600;
  color: var(--primary);
  font-size: var(--font-base);
}

.stock-warning {
  color: #dc3545;
  font-size: var(--font-xs);
  margin-top: 0.5rem;
  font-weight: 500;
}

.cart-item-quantity {
  margin: 0 1.5rem;
  min-width: 120px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 10px;
  padding: 0.25rem;
}

.quantity-selector .btn {
  padding: 0.25rem 0.5rem;
  border: none;
  background-color: transparent;
  color: var(--primary-dark);
  transition: all 0.2s ease;
  font-size: var(--font-sm);
}

.quantity-selector .btn:hover:not(:disabled) {
  background-color: var(--accent);
  color: white;
}

.quantity-selector .form-control {
  width: 50px;
  text-align: center;
  margin: 0 0.25rem;
  padding: 0.25rem;
  border: none;
  background-color: transparent;
  font-weight: 600;
  color: var(--primary-dark);
  font-size: var(--font-sm);
}

.cart-item-total {
  font-weight: 700;
  color: var(--primary-dark);
  margin: 0 1rem;
  min-width: 80px;
  text-align: right;
  font-size: var(--font-md);
}

.cart-item-actions .btn {
  padding: 0.35rem 0.6rem;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-size: var(--font-sm);
}

.cart-item-actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-footer {
  background-color: white;
  border-top: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.cart-summary {
  border-radius: 16px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 20px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  color: #666;
  font-size: var(--font-sm);
}

.summary-divider {
  height: 1px;
  background-color: #f0f0f0;
  margin: 1.25rem 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-weight: 700;
  font-size: var(--font-lg);
  color: var(--primary-dark);
}

.promo-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
}

.promo-success {
  margin-top: 0.75rem;
  color: #28a745;
  font-size: var(--font-sm);
  display: flex;
  align-items: center;
}

.invalid-feedback {
  display: block;
  margin-top: 0.5rem;
  font-size: var(--font-xs);
  color: #dc3545;
}

.checkout-warning {
  color: #dc3545;
  font-size: var(--font-sm);
  text-align: center;
}

.btn-primary {
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  border: none;
  padding: 0.85rem 1.5rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 104, 132, 0.2);
  transition: all 0.3s ease;
  font-size: var(--font-base);
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

.btn-outline-primary {
  color: var(--primary);
  border-color: var(--primary);
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: var(--font-base);
}

.btn-outline-primary:hover {
  background-color: var(--primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: var(--font-base);
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Modal styling */
.modal-content {
  border-radius: 16px;
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.modal-header .modal-title {
  color: var(--primary-dark);
  font-weight: 600;
  font-size: var(--font-lg);
}

.modal-body {
  padding: 1.5rem;
  font-size: var(--font-base);
}

.modal-footer {
  background-color: white;
  border-top: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

/* Hide number input arrows */
.quantity-selector input[type="number"]::-webkit-inner-spin-button,
.quantity-selector input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.quantity-selector input[type="number"] {
  -moz-appearance: textfield;
}

/* Responsive font scaling */
@media (max-width: 1200px) {
  :root {
    --font-3xl: 1.75rem;  /* 28px */
    --font-2xl: 1.5rem;   /* 24px */
    --font-xl: 1.25rem;   /* 20px */
    --font-lg: 1.125rem;  /* 18px */
    --font-md: 1rem;      /* 16px */
  }
}

/* Tablet and small desktop */
@media (max-width: 992px) {
  :root {
    --font-3xl: 1.5rem;   /* 24px */
    --font-2xl: 1.25rem;  /* 20px */
    --font-xl: 1.125rem;  /* 18px */
    --font-lg: 1rem;      /* 16px */
  }
  
  .cart-summary {
    margin-top: 1.5rem;
  }
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  :root {
    --font-3xl: 1.25rem;  /* 20px */
    --font-2xl: 1.125rem; /* 18px */
    --font-xl: 1rem;      /* 16px */
    --font-lg: 0.9375rem; /* 15px */
    --font-md: 0.9375rem; /* 15px */
    --font-base: 0.875rem;/* 14px */
    --font-sm: 0.8125rem; /* 13px */
    --font-xs: 0.75rem;   /* 12px */
  }
  
  .cart-item {
    flex-wrap: wrap;
    padding: 1.25rem;
    position: relative;
    padding-bottom: 3.5rem;
  }
  
  .cart-item-image {
    width: 70px;
    height: 70px;
    margin-right: 1rem;
  }
  
  .cart-item-details {
    width: calc(100% - 85px);
    margin-bottom: 0.75rem;
  }
  
  .cart-item-name {
    font-size: var(--font-base);
  }
  
  .cart-item-description {
    font-size: var(--font-sm);
    -webkit-line-clamp: 1;
  }
  
  .cart-item-price {
    font-size: var(--font-sm);
    position: absolute;
    left: 85px;
    bottom: 1.25rem;
  }
  
  .cart-item-quantity {
    order: 3;
    margin: 0.5rem 0 0 0;
    width: 100%;
  }
  
  .cart-item-total {
    order: 4;
    margin: 0;
    position: absolute;
    right: 1.25rem;
    bottom: 1.25rem;
    text-align: right;
    min-width: auto;
    font-size: var(--font-base);
  }
  
  .cart-item-actions {
    position: absolute;
    right: 1.25rem;
    top: 1.25rem;
  }
  
  .quantity-selector {
    justify-content: flex-start;
    width: 7.6rem;
  }
  
  .quantity-selector .form-control {
    width: 40px;
  }
  
  .cart-summary {
    margin-top: 1.5rem;
    position: static;
  }
  
  .card-footer .btn {
    padding: 0.75rem 1rem;
    font-size: var(--font-base);
  }
}

/* Small mobile devices */
@media (max-width: 576px) {
  :root {
    --font-3xl: 1.125rem; /* 18px */
    --font-2xl: 1rem;     /* 16px */
    --font-xl: 0.9375rem; /* 15px */
  }
  
  .empty-cart {
    min-height: 250px;
  }
  
  .empty-cart i {
    font-size: var(--font-2xl);
  }
  
  .empty-cart h3 {
    font-size: var(--font-xl);
  }
  
  .empty-cart p {
    font-size: var(--font-sm);
  }
  
  .empty-cart .btn {
    width: 100%;
  }
  
  .cart-item {
    padding: 1rem;
    padding-bottom: 3rem;
  }
  
  .cart-item-image {
    width: 60px;
    height: 60px;
  }
  
  .cart-item-details {
    width: calc(100% - 75px);
  }
  
  .cart-item-price {
    left: 5.7rem;
    bottom: 6.4rem;
  }
  
  .cart-item-total {
    right: 1rem;
    bottom: 1rem;
  }

  .quantity-selector{
    width: 7.6rem;
  }
  
  .cart-item-actions {
    right: 1rem;
    top: 1rem;
  }
  
  .card-footer .d-flex {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .card-footer .btn {
    width: 100%;
  }
}

/* Very small devices (phones less than 400px) */
@media (max-width: 400px) {
  :root {
    --font-3xl: 1rem;     /* 16px */
    --font-2xl: 0.9375rem;/* 15px */
    --font-xl: 0.875rem;  /* 14px */
  }
  
  .cart-item {
    padding-bottom: 3.5rem;
  }
  
  .cart-item-quantity {
    margin-top: 0.75rem;
  }
  
  .cart-item-price {
    bottom: 7rem;
    left: 5.7rem;
  }

  .quantity-selector{
    width: 7rem;
  }

  .quantity-selector .btn,
  .quantity-selector .form-control {
    padding: 0.2rem 0.4rem;
  }
  
  .btn-primary,
  .btn-outline-primary,
  .btn-outline-danger {
    padding: 0.75rem;
    font-size: var(--font-sm);
  }
}
</style>