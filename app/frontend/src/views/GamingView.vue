<template>
  <div class="gaming-view">
    <div class="container">
      <h1 class="title">Spiele</h1>
      <p class="subtitle">Wähle ein Spiel aus</p>

      <div class="games-grid">
        <!-- Games will be added here later -->
        <div class="coming-soon">
          <h3>Spiele kommen bald!</h3>
          <p>Hier werden verschiedene Namensspiele verfügbar sein.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Gaming functionality will be implemented later
</script>

<style scoped>
.gaming-view {
  padding: 2rem;
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
}

.games-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.coming-soon {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  grid-column: 1 / -1;
}

.coming-soon h3 {
  color: #007bff;
  margin-bottom: 1rem;
}

.coming-soon p {
  color: #666;
}

@media (max-width: 768px) {
  .gaming-view {
    padding: 1rem;
  }

  .title {
    font-size: 1.5rem;
  }
}
</style>
