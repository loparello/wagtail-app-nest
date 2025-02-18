import { ref, computed } from 'vue';
import type { MenuItem } from '../types/menu';

export function useSubmenu(item: MenuItem) {
  // Reactive state
  const showSubmenu = ref(false);

  // Computed properties
  const hasSubmenu = computed(() => item.has_submenu);
  const submenuItems = computed(() => item.submenu_items);

  // Methods
  const toggleSubmenu = () => {
    showSubmenu.value = !showSubmenu.value;
  };

  const forceToggleSubmenu = (show: boolean = false) => {
    showSubmenu.value = show;
  };

  return {
    showSubmenu,
    hasSubmenu,
    submenuItems,
    toggleSubmenu,
    forceToggleSubmenu,
  };
}
