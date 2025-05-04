<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="hero-title">Welcome to <span>E-Store</span></h1>
            <p class="hero-subtitle">Discover amazing products at unbeatable prices</p>
            <div class="hero-buttons">
              <router-link to="/products" class="btn btn-primary btn-lg">
                <i class="bi bi-shop me-2"></i>Browse Products
              </router-link>
              <router-link to="/login" class="btn btn-outline-primary btn-lg ms-2">
                <i class="bi bi-person me-2"></i>Sign In
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 d-none d-lg-block">
            <div class="hero-image">
              <img src="/img/hero-image.svg" alt="Shopping illustration" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title text-center mb-5">Why Choose Us</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-truck"></i>
              </div>
              <h3>Fast Delivery</h3>
              <p>Get your products delivered to your doorstep quickly and efficiently.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-shield-check"></i>
              </div>
              <h3>Secure Payments</h3>
              <p>Shop with confidence with our secure payment options.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="bi bi-arrow-counterclockwise"></i>
              </div>
              <h3>Easy Returns</h3>
              <p>Not satisfied? Return your products hassle-free within 30 days.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>Ready to start shopping?</h2>
          <p>Create an account today and get access to exclusive deals and offers.</p>
          <router-link to="/register" class="btn btn-light btn-lg">
            <i class="bi bi-person-plus me-2"></i>Create Account
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home-container {
  overflow-x: hidden;
}

.hero-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: var(--light);
  position: relative;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-title span {
  color: var(--accent);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-buttons {
  margin-bottom: 2rem;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
  animation: float 6s ease-in-out infinite;
}

.hero-image img {
  max-width: 100%;
  height: auto;
}

.features-section {
  padding: 5rem 0;
  background-color: white;
}

.section-title {
  color: var(--primary-dark);
  font-weight: 700;
  margin-bottom: 3rem;
}

.feature-card {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 2rem;
  text-align: center;
  box-shadow: var(--box-shadow);
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--accent);
  color: var(--primary-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin: 0 auto 1.5rem;
}

.feature-card h3 {
  color: var(--primary-dark);
  font-weight: 600;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  margin-bottom: 0;
}

.cta-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
  color: var(--light);
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

@media (max-width: 992px) {
  .hero-section {
    padding: 3rem 0;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .features-section, .cta-section {
    padding: 3rem 0;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-  .cta-section {
    padding: 3rem 0;
  }
}
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-buttons .btn {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .hero-buttons .btn:last-child {
    margin-left: 0 !important;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
}
</style>