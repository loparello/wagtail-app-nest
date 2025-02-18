<template>
  <div class="main-menu navbar-menu" :class="{ 'navbar-collapse': collapseMenu }">
    <ul class="menu-nav">
      <template v-for="item in menuItems">
        <menu-category
          v-if="checkIsMenuCategory(item)"
          :key="'category-' + item.id"
          :item="item"
        />
        <menu-link v-else :key="'link-' + item.id" :item="item" />
      </template>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { computed, PropType } from 'vue';
import type { Menu, MenuItem } from '../../types/menu';
import MenuLink from './MenuLink.vue';
import MenuCategory from './MenuCategory.vue';

// Props
const props = defineProps({
  menu: {
    type: Object as PropType<Menu>,
    required: true,
  },
  collapseMenu: {
    type: Boolean,
    default: false,
  },
});

// Computed properties
const menuItems = computed(() => props.menu.menu_items);

// Methods
const checkIsMenuCategory = (item: MenuItem) => {
  return item.type === 'menu_category';
};
</script>
