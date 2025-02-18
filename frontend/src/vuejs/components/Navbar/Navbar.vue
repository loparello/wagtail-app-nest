<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-logo">
      <a href="/">
        <!-- <img
          src="../../../img/logo.svg"
          alt="Logo"
          class="navbar-logo-figure"
        /> -->
        <span>Wagtail App Nest</span>
      </a>
    </div>

    <!-- Desktop menu -->
    <main-menu :menu="menu" />

    <menu-toggler @toggle-menu="toggleMenu" />
    <!-- Mobile/Tablet menu -->
    <transition-collapse>
      <main-menu :menu="menu" collapseMenu v-show="showMenu" />
    </transition-collapse>
  </nav>
</template>

<script lang="ts" setup>
import { ref, PropType } from 'vue';
import type { Menu } from '../../types/menu';
import MainMenu from '../MainMenu/MainMenu.vue';
import TransitionCollapse from '../Transitions/TransitionCollapse.vue';
import MenuToggler from './MenuToggler.vue';

// Props
defineProps({
  menu: {
    type: Object as PropType<Menu>,
    required: true,
  },
});

// Reactive state
const showMenu = ref(false);

// Methods
const toggleMenu = (show: boolean) => {
  showMenu.value = show;
};
</script>
