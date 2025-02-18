export interface MenuItemLink {
  url: string;
  target: string;
}

export interface MenuItem {
  id: string;
  type: string;
  label: string;
  handle: string;
  active: boolean;
  link: MenuItemLink;
  has_submenu: boolean;
  is_submenu_item: boolean;
  submenu_items: MenuItem[];
}

export interface Menu {
  id: number;
  name: string;
  handle: string;
  heading: string;
  is_main: boolean;
  menu_items: MenuItem[];
}
