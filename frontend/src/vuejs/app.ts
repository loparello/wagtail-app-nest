import { createApp } from 'vue';
import HomeHero from './components/HomeHero.vue';
import Navbar from './components/Navbar/Navbar.vue';

export default function mountVueApps() {
  // Example home hero app
  const homeHeroContainer = document.getElementById('vHomeHero');
  if (homeHeroContainer) {
    const homeHeroApp = createApp(HomeHero);
    homeHeroApp.mount(homeHeroContainer);
  }

  // Navbar app
  const NavbarContainer = document.getElementById('vNavbar');
  const mainMenuDataEl = document.getElementById('mainMenuData');

  if (NavbarContainer && mainMenuDataEl) {
    const mainMenuData = JSON.parse(
      mainMenuDataEl.textContent ? mainMenuDataEl.textContent : '',
    );
    mainMenuDataEl.remove();
    const navbarApp = createApp(Navbar, { menu: mainMenuData });
    navbarApp.mount(NavbarContainer);
  }
}
