<template>
  <button
    @click="toggle"
    class="relative flex flex-col items-center justify-center w-10 h-10 gap-1.5 bg-primary border-none rounded cursor-pointer lg:hidden"
    title="Navigation toggle"
  >
    <span
      class="block bg-white w-6 h-0.5 rounded-sm transition-all duration-250 origin-center"
      :class="show ? 'rotate-45 translate-y-2' : ''"
    />
    <span
      class="block bg-white w-6 h-0.5 rounded-sm transition-all duration-250"
      :class="show ? 'opacity-0 scale-x-0' : ''"
    />
    <span
      class="block bg-white w-6 h-0.5 rounded-sm transition-all duration-250 origin-center"
      :class="show ? '-rotate-45 -translate-y-2' : ''"
    />
  </button>
</template>

<script lang="ts" setup>
import { ref } from "vue";

// Reactive state
const show = ref(false);

// Emit event
const emit = defineEmits(["toggle-menu"]);

// Methods
const toggle = () => {
  show.value = !show.value;
  emit("toggle-menu", show.value);
};
</script>
