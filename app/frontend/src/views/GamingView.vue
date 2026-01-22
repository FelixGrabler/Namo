<template>
  <div class="min-h-screen bg-slate-50">
    <div class="max-w-5xl mx-auto px-6 py-10">
      <header class="text-center mb-10">
        <h1 class="text-3xl font-bold text-slate-900">Spiele</h1>
        <p class="text-slate-600 mt-2">Wähle ein Namensspiel aus.</p>
      </header>

      <div class="grid gap-6 md:grid-cols-2">
        <router-link
          to="/games/higher-lower"
          class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition"
        >
          <p class="text-xs uppercase tracking-[0.25em] text-slate-500">Ranking</p>
          <h2 class="text-2xl font-bold text-slate-900 mt-2">Higher or Lower</h2>
          <p class="text-sm text-slate-600 mt-2">
            Rate, welcher Name 2023 in Österreich häufiger vergeben wurde.
          </p>
        </router-link>

        <router-link
          to="/games/wordle"
          class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition"
        >
          <p class="text-xs uppercase tracking-[0.25em] text-slate-500">Wortspiel</p>
          <h2 class="text-2xl font-bold text-slate-900 mt-2">Name Wordle</h2>
          <p class="text-sm text-slate-600 mt-2">
            Errate den geheimen 5-Buchstaben-Namen in sechs Versuchen.
          </p>
        </router-link>
      </div>
    </div>
  </div>
</template>
