<template>
  <div class="hero">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1>{{ title }}</h1>
          <p>{{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";

// Reactive state
const title = ref("Welcome to Wagtail App Nest");
const message = ref("A template for new Django and Wagtail CMS applications");

// Lifecycle hook
onMounted(() => {
  console.log("Home Hero component mounted with Vue.js");
});
</script>
