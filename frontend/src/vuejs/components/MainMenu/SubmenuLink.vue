<template>
  <li :id="item.handle" class="submenu-item">
    <a
      :href="item.link && item.link.url"
      :target="item.link && item.link.target"
      class="submenu-item-link"
      :class="{ active: item.active }"
    >
      {{ item.label }}
    </a>

    <submenu v-if="hasSubmenu" :submenu-items="submenuItems" />
  </li>
</template>

<script lang="ts" setup>
import { PropType } from 'vue';
import type { MenuItem } from '../../types/menu';
import { useSubmenu } from '../../composables/submenu';
import Submenu from './Submenu.vue';

// Props
const props = defineProps({
  item: {
    type: Object as PropType<MenuItem>,
    required: true,
  },
});

const { hasSubmenu, submenuItems } = useSubmenu(props.item);
</script>
