<template>
  <div class="product-catalog container">
    <div class="catalog-header">
      <h2 class="section-title">
        <i class="bi bi-shop me-2"></i>Discover Our Collection
      </h2>
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search products..." 
          class="search-input"
          aria-label="Search products"
        />
        <i class="bi bi-search search-icon"></i>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner">
        <div class="bounce1"></div>
        <div class="bounce2"></div>
        <div class="bounce3"></div>
      </div>
      <p>Loading products...</p>
    </div>

    <div v-else-if="filteredProducts.length === 0" class="empty-products">
      <i class="bi bi-search-heart"></i>
      <h3>No products found</h3>
      <p>We couldn't find any products matching your search.</p>
      <button class="btn btn-primary mt-3" @click="resetSearch">
        <i class="bi bi-arrow-counterclockwise me-2"></i>View All Products
      </button>
    </div>

    <div v-else>
      <div class="product-count">
        <span>{{ filteredProducts.length }} products</span>
      </div>
      
      <div class="product-grid">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id" 
          class="product-card"
          :class="{ 'out-of-stock': product.stock === 0 }"
        >
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
            
            <div class="product-badges">
              <div v-if="product.stock === 0" class="stock-badge out-of-stock-badge">
                Out of Stock
              </div>
              <div v-else-if="product.stock < 5" class="stock-badge low-stock-badge">
                Only {{ product.stock }} left!
              </div>
              <div v-if="isNewProduct(product)" class="stock-badge new-badge">
                New
              </div>
            </div>
          </div>
          
          <div class="product-details">
            <div class="product-rating">
              <div class="stars">
                <i v-for="n in 5" :key="n" class="bi" :class="n <= getProductRating(product) ? 'bi-star-fill' : 'bi-star'"></i>
              </div>
              <span class="rating-count">({{ getReviewCount(product) }})</span>
            </div>
            
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-description">{{ truncate(product.description, 80) }}</p>
            
            <div class="product-price">₱{{ formatPrice(product.price) }}</div>
            
            <div class="product-actions" v-if="product.stock > 0">
              <div class="quantity-selector">
                <button 
                  class="quantity-btn" 
                  @click="decrementQuantity(product)"
                  :disabled="quantities[product.id] <= 1"
                  aria-label="Decrease quantity"
                >
                  <i class="bi bi-dash"></i>
                </button>
                <span class="quantity">{{ quantities[product.id] || 1 }}</span>
                <button 
                  class="quantity-btn" 
                  @click="incrementQuantity(product)"
                  :disabled="quantities[product.id] >= product.stock"
                  aria-label="Increase quantity"
                >
                  <i class="bi bi-plus"></i>
                </button>
              </div>
              
              <button 
                class="add-to-cart-btn" 
                @click="addToCart(product)"
                aria-label="Add to cart"
              >
                <i class="bi bi-cart-plus me-2"></i>Add to Cart
              </button>
            </div>
            
            <button 
              v-else
              class="out-of-stock-btn" 
              disabled
              aria-label="Out of stock"
            >
              Out of Stock
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
import { useToastStore } from '../stores/toastStore'

export default {
  setup() {
    const products = ref([])
    const isLoading = ref(true)
    const searchQuery = ref('')
    const toast = useToastStore()
    const quantities = reactive({})
    
    // Notify other components about cart updates
    const notifyCartUpdate = () => {
      // Dispatch a custom event that App.vue listens for
      window.dispatchEvent(new CustomEvent('cart-updated'))
    }
    
    const filteredProducts = computed(() => {
      if (!searchQuery.value) return products.value
      
      const query = searchQuery.value.toLowerCase()
      return products.value.filter(product => 
        product.name.toLowerCase().includes(query) || 
        product.description.toLowerCase().includes(query)
      )
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
    
    const resetSearch = () => {
      searchQuery.value = ''
    }
    
    // Generate a consistent rating for each product based on its ID
    const getProductRating = (product) => {
      // Use product ID to generate a consistent rating between 3 and 5
      return ((product.id * 7) % 3) + 3; // 3, 4, or 5
    }
    
    // Generate a random but consistent number of reviews
    const getReviewCount = (product) => {
      // Use product ID to generate a consistent number between 5 and 120
      return ((product.id * 7) % 115) + 5;
    }
    
    // Check if product is "new" (for demo purposes, consider some products as new)
    const isNewProduct = (product) => {
      // For demo, mark every 4th product as new
      return product.id % 4 === 0;
    }
    
    const incrementQuantity = (product) => {
      if (!quantities[product.id]) {
        quantities[product.id] = 1
      }
      
      if (quantities[product.id] < product.stock) {
        quantities[product.id]++
      }
    }
    
    const decrementQuantity = (product) => {
      if (!quantities[product.id]) {
        quantities[product.id] = 1
      }
      
      if (quantities[product.id] > 1) {
        quantities[product.id]--
      }
    }
    
    const fetchProducts = async () => {
      isLoading.value = true
      try {
        const response = await axios.get('products/')
        products.value = response.data
        
        // Initialize quantities
        products.value.forEach(product => {
          quantities[product.id] = 1
        })
      } catch (error) {
        console.error('Error fetching products:', error)
        toast.error('Failed to load products. Please try again.')
      } finally {
        isLoading.value = false
      }
    }
    
    const addToCart = (product) => {
      if (product.stock === 0) {
        toast.error('Sorry, this product is out of stock.')
        return
      }
      
      try {
        // Get existing cart from localStorage
        let cart = []
        const savedCart = localStorage.getItem('cart')
        
        if (savedCart) {
          cart = JSON.parse(savedCart)
        }
        
        // Check if product already in cart
        const existingItem = cart.find(item => item.product && item.product.id === product.id)
        const quantityToAdd = quantities[product.id] || 1
        
        if (existingItem) {
          // Check if adding the quantity would exceed stock
          if (existingItem.quantity + quantityToAdd <= product.stock) {
            existingItem.quantity += quantityToAdd
            toast.success(`Added ${quantityToAdd} ${product.name} to your cart.`)
          } else {
            toast.warning(`Cannot add ${quantityToAdd} more ${product.name}. Maximum stock reached.`)
            return
          }
        } else {
          // Add new item to cart
          cart.push({
            product: {
              id: product.id,
              name: product.name,
              price: product.price,
              description: product.description,
              image: product.image,
              stock: product.stock
            },
            quantity: quantityToAdd
          })
          toast.success(`Added ${quantityToAdd} ${product.name} to your cart!`)
        }
        
        // Save updated cart
        localStorage.setItem('cart', JSON.stringify(cart))
        
        // Reset quantity after adding to cart
        quantities[product.id] = 1
        
        // Trigger storage event for other components to detect
        window.dispatchEvent(new Event('storage'))
        
        // Notify about cart update
        notifyCartUpdate()
      } catch (err) {
        console.error('Error adding to cart:', err)
        toast.error('Failed to add product to cart.')
      }
    }
    
    onMounted(() => {
      fetchProducts()
    })
    
    return {
      products,
      filteredProducts,
      isLoading,
      searchQuery,
      quantities,
      fullImageUrl,
      formatPrice,
      truncate,
      resetSearch,
      addToCart,
      incrementQuantity,
      decrementQuantity,
      getProductRating,
      getReviewCount,
      isNewProduct
    }
  }
}
</script>

<style scoped>
:root {
  --primary: #006884;
  --primary-dark: #053D57;
  --primary-light: #97BCC7;
  --light: #F2F1EF;
  --accent: #97BCC7;
  --text-dark: #2D3748;
  --text-light: #718096;
  --success: #48BB78;
  --warning: #F6AD55;
  --danger: #F56565;
  --background: #F7FAFC;
  --card-bg: #FFFFFF;
}

.product-catalog {
  padding: 2rem 0;
  background-color: var(--background);
  min-height: 80vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.catalog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 0;
  font-size: 1.75rem;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 3px;
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
  padding: 0.6rem 1rem;
  padding-right: 2.5rem;
  transition: all 0.3s ease;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 104, 132, 0.15);
  outline: none;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  font-size: 1rem;
}

.product-count {
  margin-bottom: 1.5rem;
  color: var(--primary-dark);
  font-size: 0.95rem;
  font-weight: 500;
}

/* Loading animation */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  padding: 2rem;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
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
  margin-top: 1rem;
}

.empty-products {
  text-align: center;
  padding: 3rem 1rem;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.empty-products i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--accent);
  opacity: 0.8;
}

.empty-products h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--primary-dark);
}

.empty-products p {
  color: #666;
  max-width: 300px;
  margin: 0 auto 1.5rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background-color: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.product-card.out-of-stock {
  opacity: 0.8;
}

.product-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #ccc;
  font-size: 3rem;
}

.product-badges {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 2;
}

.stock-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.out-of-stock-badge {
  background-color: #dc3545;
}

.low-stock-badge {
  background-color: #ffc107;
  color: #212529;
}

.new-badge {
  background-color: #28a745;
}

.product-details {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.product-rating {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.stars {
  display: flex;
  color: #ffc107;
  font-size: 0.85rem;
}

.stars i {
  margin-right: 2px;
}

.rating-count {
  margin-left: 5px;
  font-size: 0.8rem;
  color: #6c757d;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #212529;
  line-height: 1.3;
}

.product-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.5;
  flex-grow: 1;
}

.product-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 1rem;
}

.product-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quantity-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 0.25rem;
  margin-bottom: 0.5rem;
}

.quantity-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background-color: white;
  color: #495057;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.quantity-btn:hover:not(:disabled) {
  background-color: var(--primary);
  color: white;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  font-weight: 600;
  color: #212529;
  min-width: 30px;
  text-align: center;
}

.add-to-cart-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #006884 0%, #053D57 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 104, 132, 0.2);
}

.add-to-cart-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 104, 132, 0.3);
}

.add-to-cart-btn:active {
  transform: translateY(1px);
}

.out-of-stock-btn {
  width: 100%;
  padding: 0.75rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: not-allowed;
  opacity: 0.8;
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

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 104, 132, 0.3);
}

/* Mobile responsiveness */
@media (max-width: 992px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}

@media (max-width: 768px) {
  .catalog-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-container {
    width: 100%;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.25rem;
  }
  
  .product-image {
    height: 180px;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.5rem;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
  
  .product-details {
    padding: 1rem;
  }
  
  .product-name {
    font-size: 1rem;
  }
  
  .product-description {
    font-size: 0.85rem;
  }
  
  .product-price {
    font-size: 1.1rem;
  }
  
  .add-to-cart-btn, .out-of-stock-btn {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}
</style>