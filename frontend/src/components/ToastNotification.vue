<template>
    <div class="toast-container">
      <transition-group name="toast">
        <div 
          v-for="toast in toasts" 
          :key="toast.id" 
          class="toast-notification" 
          :class="[
            `toast-${toast.type}`,
            { 'toast-visible': toast.visible }
          ]"
          role="alert"
          aria-live="assertive"
        >
          <div class="toast-icon">
            <i 
              class="bi" 
              :class="{
                'bi-check-circle-fill': toast.type === 'success',
                'bi-exclamation-triangle-fill': toast.type === 'warning',
                'bi-x-circle-fill': toast.type === 'error',
                'bi-info-circle-fill': toast.type === 'info'
              }"
            ></i>
          </div>
          <div class="toast-content">
            <p class="toast-message">{{ toast.message }}</p>
          </div>
          <button 
            class="toast-close" 
            @click="removeToast(toast.id)"
            aria-label="Close notification"
          >
            <i class="bi bi-x"></i>
          </button>
          <div 
            class="toast-progress" 
            :style="{ animationDuration: `${toast.duration}ms` }"
          ></div>
        </div>
      </transition-group>
    </div>
  </template>
  
  <script>
  import { useToastStore } from '../stores/toastStore'
  
  export default {
    setup() {
      const { toasts, removeToast } = useToastStore()
      
      return {
        toasts,
        removeToast
      }
    }
  }
  </script>
  
  <style scoped>
  .toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 100%;
    width: 350px;
    pointer-events: none;
  }
  
  .toast-notification {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    padding: 12px 15px;
    display: flex;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.3s ease;
    pointer-events: auto;
    max-width: 100%;
  }
  
  .toast-visible {
    opacity: 1;
    transform: translateX(0);
  }
  
  .toast-icon {
    flex-shrink: 0;
    font-size: 1.25rem;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .toast-content {
    flex-grow: 1;
    padding-right: 10px;
  }
  
  .toast-message {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.4;
    word-break: break-word;
  }
  
  .toast-close {
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    color: #666;
    opacity: 0.7;
    transition: opacity 0.2s;
    flex-shrink: 0;
  }
  
  .toast-close:hover {
    opacity: 1;
  }
  
  .toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.3);
    transform-origin: left;
    animation: progress-bar linear forwards;
  }
  
  @keyframes progress-bar {
    from {
      transform: scaleX(1);
    }
    to {
      transform: scaleX(0);
    }
  }
  
  /* Toast types */
  .toast-success {
    border-left: 4px solid #28a745;
  }
  
  .toast-success .toast-icon {
    color: #28a745;
  }
  
  .toast-success .toast-progress {
    background-color: #28a745;
  }
  
  .toast-warning {
    border-left: 4px solid #ffc107;
  }
  
  .toast-warning .toast-icon {
    color: #ffc107;
  }
  
  .toast-warning .toast-progress {
    background-color: #ffc107;
  }
  
  .toast-error {
    border-left: 4px solid #dc3545;
  }
  
  .toast-error .toast-icon {
    color: #dc3545;
  }
  
  .toast-error .toast-progress {
    background-color: #dc3545;
  }
  
  .toast-info {
    border-left: 4px solid #17a2b8;
  }
  
  .toast-info .toast-icon {
    color: #17a2b8;
  }
  
  .toast-info .toast-progress {
    background-color: #17a2b8;
  }
  
  /* Toast animations */
  .toast-enter-active,
  .toast-leave-active {
    transition: all 0.3s ease;
  }
  
  .toast-enter-from {
    opacity: 0;
    transform: translateX(100%);
  }
  
  .toast-leave-to {
    opacity: 0;
    transform: translateX(100%);
  }
  
  /* Mobile responsiveness */
  @media (max-width: 576px) {
    .toast-container {
      top: 10px;
      right: 10px;
      left: 10px;
      width: auto;
    }
    
    .toast-notification {
      padding: 10px 12px;
      border-radius: 6px;
    }
    
    .toast-icon {
      font-size: 1.1rem;
      margin-right: 10px;
    }
    
    .toast-message {
      font-size: 0.9rem;
    }
    
    .toast-close {
      font-size: 0.9rem;
    }
    
    .toast-progress {
      height: 2px;
    }
  }
  
  /* For very small screens */
  @media (max-width: 360px) {
    .toast-container {
      top: 45px;
      right: 5px;
      left: 4.6rem;
      width: 15rem;
    }
    
    .toast-notification {
      padding: 8px 10px;
    }
    
    .toast-icon {
      font-size: 1rem;
      margin-right: 8px;
    }
    
    .toast-message {
      font-size: 0.85rem;
    }
  }
  </style>