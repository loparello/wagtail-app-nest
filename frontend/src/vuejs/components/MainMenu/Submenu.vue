<template>
  <ul class="submenu controlled">
    <submenu-link v-for="item in submenuItems" :key="item.id" :item="item" />
  </ul>
</template>

<script lang="ts" setup>
import { PropType } from 'vue';
import type { MenuItem } from '../../types/menu';
import SubmenuLink from './SubmenuLink.vue';

// Props
defineProps({
  submenuItems: {
    type: Array as PropType<MenuItem[]>,
    required: true,
  },
});
</script>
