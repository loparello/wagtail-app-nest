<template>
  <ul
    class="bg-primary py-2 list-none m-0 w-full lg:absolute lg:border lg:border-black/15 lg:rounded lg:min-w-40 lg:w-auto lg:z-1000"
  >
    <submenu-link v-for="item in submenuItems" :key="item.id" :item="item" />
  </ul>
</template>

<script lang="ts" setup>
import { PropType } from "vue";
import type { MenuItem } from "../../types/menu";
import SubmenuLink from "./SubmenuLink.vue";

// Props
defineProps({
  submenuItems: {
    type: Array as PropType<MenuItem[]>,
    required: true,
  },
});
</script>
