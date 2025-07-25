<template>
  <div class="desktop-nav">
    <!-- Burger Menu Button -->
    <button
      @click="toggleMenu"
      class="menu-button"
      :class="{ active: isMenuOpen }"
    >
      <div class="burger-lines">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </button>

    <!-- Menu Overlay -->
    <div
      v-if="isMenuOpen"
      @click="closeMenu"
      class="menu-overlay"
    ></div>

    <!-- Vertical Menu -->
    <nav
      class="menu"
      :class="{ open: isMenuOpen }"
    >
      <div class="menu-header">
        <h3>Navigation</h3>
        <button @click="closeMenu" class="close-button">×</button>
      </div>

      <div class="menu-items">
        <router-link
          to="/vote"
          @click="closeMenu"
          class="menu-item"
          :class="{ active: $route.name === 'Vote' }"
        >
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"/>
            </svg>
          </div>
          <span>Startseite</span>
        </router-link>

        <router-link
          to="/games"
          @click="closeMenu"
          class="menu-item"
          :class="{ active: $route.name === 'Gaming' }"
        >
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M7.97,16L5,19C4.67,19.3 4.23,19.5 3.75,19.5A1.75,1.75 0 0,1 2,17.75V17.5L3,10.12C3.21,7.81 5.14,6 7.5,6H16.5C18.86,6 20.79,7.81 21,10.12L22,17.5V17.75A1.75,1.75 0 0,1 20.25,19.5C19.77,19.5 19.33,19.3 19,19L16.03,16H7.97M7,8V10H5V11H7V13H8V11H10V10H8V8H7M16.5,8A0.75,0.75 0 0,0 15.75,8.75A0.75,0.75 0 0,0 16.5,9.5A0.75,0.75 0 0,0 17.25,8.75A0.75,0.75 0 0,0 16.5,8M14.75,9.75A0.75,0.75 0 0,0 14,10.5A0.75,0.75 0 0,0 14.75,11.25A0.75,0.75 0 0,0 15.5,10.5A0.75,0.75 0 0,0 14.75,9.75Z"/>
            </svg>
          </div>
          <span>Spiele</span>
        </router-link>

        <router-link
          to="/account"
          @click="closeMenu"
          class="menu-item"
          :class="{ active: $route.name === 'Account' }"
        >
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
            </svg>
          </div>
          <span>Persönliches</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<style scoped>
.desktop-nav {
  position: relative;
}

/* Menu Button */
.menu-button {
  position: fixed;
  top: 2rem;
  left: 2rem;
  width: 50px;
  height: 50px;
  background: #007bff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1001;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

.menu-button:hover {
  background: #0056b3;
  transform: scale(1.05);
}

.menu-button.active {
  background: #dc3545;
}

.burger-lines {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.burger-lines span {
  display: block;
  width: 20px;
  height: 2px;
  background: white;
  margin: 2px 0;
  transition: all 0.3s ease;
}

.menu-button.active .burger-lines span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.menu-button.active .burger-lines span:nth-child(2) {
  opacity: 0;
}

.menu-button.active .burger-lines span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

/* Menu Overlay */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 999;
}

/* Vertical Menu */
.menu {
  position: fixed;
  top: 0;
  left: -300px;
  width: 280px;
  height: 100vh;
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  transition: left 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
}

.menu.open {
  left: 0;
}

.menu-header {
  padding: 2rem 1.5rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #333;
}

.menu-items {
  padding: 1rem 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s;
  gap: 1rem;
}

.menu-item:hover {
  background: #f8f9fa;
}

.menu-item.active {
  background: #e3f2fd;
  color: #007bff;
  border-right: 3px solid #007bff;
}

.menu-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.menu-icon svg {
  width: 100%;
  height: 100%;
}

.menu-item span {
  font-weight: 500;
}

/* Hide on mobile */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }
}
</style>
