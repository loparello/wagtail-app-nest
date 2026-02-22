<template>
  <li
    :id="item.handle"
    class="relative py-2 px-4"
    @mouseover="forceToggleSubmenu(true)"
    @mouseleave="forceToggleSubmenu()"
  >
    <div class="flex items-center">
      <span
        class="text-white cursor-default"
        :class="{ 'opacity-50': item.active }"
      >
        {{ item.label }}
      </span>

      <template v-if="hasSubmenu">
        <span
          class="ml-1 cursor-pointer text-white text-xs"
          @click="toggleSubmenu"
          >▾</span
        >
      </template>
    </div>

    <template v-if="hasSubmenu">
      <transition-collapse>
        <submenu v-show="showSubmenu" :submenu-items="submenuItems" />
      </transition-collapse>
    </template>
  </li>
</template>

<script lang="ts" setup>
import { PropType } from "vue";
import type { MenuItem } from "../../types/menu";
import { useSubmenu } from "../../composables/submenu";
import TransitionCollapse from "../Transitions/TransitionCollapse.vue";
import Submenu from "./Submenu.vue";

// Props
const props = defineProps({
  item: {
    type: Object as PropType<MenuItem>,
    required: true,
  },
});

const {
  showSubmenu,
  hasSubmenu,
  submenuItems,
  toggleSubmenu,
  forceToggleSubmenu,
} = useSubmenu(props.item);
</script>
