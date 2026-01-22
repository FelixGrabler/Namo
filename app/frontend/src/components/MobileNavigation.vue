<template>
  <nav class="mobile-nav">
    <router-link to="/games" class="nav-item" :class="{ active: $route.name === 'Gaming' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M7.97,16L5,19C4.67,19.3 4.23,19.5 3.75,19.5A1.75,1.75 0 0,1 2,17.75V17.5L3,10.12C3.21,7.81 5.14,6 7.5,6H16.5C18.86,6 20.79,7.81 21,10.12L22,17.5V17.75A1.75,1.75 0 0,1 20.25,19.5C19.77,19.5 19.33,19.3 19,19L16.03,16H7.97M7,8V10H5V11H7V13H8V11H10V10H8V8H7M16.5,8A0.75,0.75 0 0,0 15.75,8.75A0.75,0.75 0 0,0 16.5,9.5A0.75,0.75 0 0,0 17.25,8.75A0.75,0.75 0 0,0 16.5,8M14.75,9.75A0.75,0.75 0 0,0 14,10.5A0.75,0.75 0 0,0 14.75,11.25A0.75,0.75 0 0,0 15.5,10.5A0.75,0.75 0 0,0 14.75,9.75Z"/>
        </svg>
      </div>
      <span class="nav-label">Spiele</span>
    </router-link>

    <router-link to="/names" class="nav-item" :class="{ active: $route.name === 'NameSearch' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M9.5 3A6.5 6.5 0 0 1 16 9.5C16 11.04 15.42 12.45 14.47 13.53L19 18.06L17.59 19.47L13.06 14.94C11.98 15.89 10.56 16.47 9 16.47A6.5 6.5 0 1 1 9.5 3M9.5 5A4.5 4.5 0 1 0 14 9.5A4.5 4.5 0 0 0 9.5 5Z"/>
        </svg>
      </div>
      <span class="nav-label">Namen</span>
    </router-link>

    <router-link to="/vote" class="nav-item" :class="{ active: $route.name === 'Vote' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"/>
        </svg>
      </div>
      <span class="nav-label">Home</span>
    </router-link>

    <router-link to="/compare" class="nav-item" :class="{ active: $route.name === 'CompareVotes' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 4A4 4 0 1 1 8 8A4 4 0 0 1 12 4M6 18C6 15.79 8.69 14 12 14C15.31 14 18 15.79 18 18V20H6V18M20 7H22V9H20V7M20 11H22V13H20V11M2 7H4V9H2V7M2 11H4V13H2V11Z"/>
        </svg>
      </div>
      <span class="nav-label">Vergleich</span>
    </router-link>

    <router-link to="/voted" class="nav-item" :class="{ active: $route.name === 'VotedNames' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M19,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M7,7H17V9H7V7M7,11H17V13H7V11M7,15H14V17H7V15Z"/>
        </svg>
      </div>
      <span class="nav-label">Auswertung</span>
    </router-link>

    <router-link to="/account" class="nav-item" :class="{ active: $route.name === 'Account' }">
      <div class="nav-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
        </svg>
      </div>
      <span class="nav-label">Account</span>
    </router-link>
  </nav>
</template>

<style scoped>
.mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e0e0e0;
  display: flex;
  padding: 0.5rem 0;
  z-index: 1000;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  text-decoration: none;
  color: #666;
  transition: color 0.2s;
}

.nav-item.active {
  color: #007bff;
}

.nav-icon {
  width: 24px;
  height: 24px;
  margin-bottom: 0.25rem;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 500;
}

/* Hide on desktop */
@media (min-width: 769px) {
  .mobile-nav {
    display: none;
  }
}
</style>
