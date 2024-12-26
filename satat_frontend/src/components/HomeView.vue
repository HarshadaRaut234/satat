<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
      <div class="container">
        <a class="navbar-brand" href="#">SATAT</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/map" class="nav-link">Map</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/decode" class="nav-link">Decode</router-link>
            </li>
            <li class="nav-item">
              <a href="http://127.0.0.1:8000/decode" class="nav-link" target="_blank">Decode Backend</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <p>Hello, World!</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<!-- Include Bootstrap CSS -->
<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css");
</style>
