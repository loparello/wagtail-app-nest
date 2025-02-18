<template>
  <button
    @click="toggle"
    class="navbar-menu-toggler"
    title="Navigation toggle"
    :class="{ active: show }"
  >
    <span class="line" />
  </button>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

// Reactive state
const show = ref(false);

// Emit event
const emit = defineEmits(['toggle-menu']);

// Methods
const toggle = () => {
  show.value = !show.value;
  emit('toggle-menu', show.value);
};
</script>
