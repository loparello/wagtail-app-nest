<template>
  <li
    :id="item.handle"
    class="menu-item dropdown"
    @mouseover="forceToggleSubmenu(true)"
    @mouseleave="forceToggleSubmenu()"
  >
    <span class="menu-item-link" :class="{ active: item.active }">
      {{ item.label }}
    </span>

    <template v-if="hasSubmenu">
      <i class="menu-item-arrow" @click="toggleSubmenu" />

      <transition-collapse>
        <submenu v-show="showSubmenu" :submenu-items="submenuItems" />
      </transition-collapse>
    </template>
  </li>
</template>

<script lang="ts" setup>
import { PropType } from 'vue';
import type { MenuItem } from '../../types/menu';
import { useSubmenu } from '../../composables/submenu';
import TransitionCollapse from '../Transitions/TransitionCollapse.vue';
import Submenu from './Submenu.vue';

// Props
const props = defineProps({
  item: {
    type: Object as PropType<MenuItem>,
    required: true,
  },
});

const { showSubmenu, hasSubmenu, submenuItems, toggleSubmenu, forceToggleSubmenu } =
  useSubmenu(props.item);
</script>
