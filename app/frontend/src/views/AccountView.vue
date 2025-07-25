<template>
  <div class="account-view">
    <div class="container">
      <div class="user-info">
        <h1 class="welcome">Willkommen, {{ userStore.username }}!</h1>
      </div>

      <div class="menu-items">
        <router-link to="/voted" class="menu-item">
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M7,7H17V9H7V7M7,11H17V13H7V11M7,15H14V17H7V15Z"/>
            </svg>
          </div>
          <div class="menu-content">
            <h3>Auswertung</h3>
            <p>Deine bewerteten Namen ansehen</p>
          </div>
          <div class="menu-arrow">›</div>
        </router-link>

        <button @click="logout" class="menu-item logout-item">
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
            </svg>
          </div>
          <div class="menu-content">
            <h3>Abmelden</h3>
            <p>Aus deinem Konto abmelden</p>
          </div>
          <div class="menu-arrow">›</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/useUserStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.account-view {
  padding: 2rem;
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 600px;
  margin: 0 auto;
}

.user-info {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  text-align: center;
}

.welcome {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.menu-item {
  background: white;
  border: none;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s;
}

.menu-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.menu-icon {
  width: 40px;
  height: 40px;
  color: #007bff;
  flex-shrink: 0;
}

.menu-icon svg {
  width: 100%;
  height: 100%;
}

.menu-content {
  flex: 1;
  text-align: left;
}

.menu-content h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  color: #333;
}

.menu-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.menu-arrow {
  font-size: 1.5rem;
  color: #ccc;
  flex-shrink: 0;
}

.logout-item:hover .menu-icon {
  color: #dc3545;
}

@media (max-width: 768px) {
  .account-view {
    padding: 1rem;
  }

  .welcome {
    font-size: 1.25rem;
  }

  .menu-item {
    padding: 1rem;
  }
}
</style>
