<template>
  <template v-if="hasSubmenu">
    <li
      :id="item.handle"
      class="relative py-2 px-4"
      @mouseover="forceToggleSubmenu(true)"
      @mouseleave="forceToggleSubmenu()"
    >
      <div class="flex items-center">
        <a
          :href="item.link && item.link.url"
          :target="item.link && item.link.target"
          class="text-white hover:underline"
          :class="{ 'opacity-50': item.active }"
        >
          {{ item.label }}
        </a>
        <span
          class="ml-1 cursor-pointer text-white text-xs"
          @click="toggleSubmenu"
          >▾</span
        >
      </div>

      <transition-collapse>
        <submenu v-show="showSubmenu" :submenu-items="submenuItems" />
      </transition-collapse>
    </li>
  </template>
  <template v-else>
    <li :id="item.handle" class="py-2 px-4">
      <a
        :href="item.link && item.link.url"
        :target="item.link && item.link.target"
        class="text-white block hover:underline"
        :class="{ 'opacity-50': item.active }"
      >
        {{ item.label }}
      </a>
    </li>
  </template>
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
