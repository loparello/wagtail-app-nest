import "vite/modulepreload-polyfill";
import mountVueApps from "./vuejs/app";
import "./css/tailwind.css";
import "./scss/main.scss";

const noJsElements = document.querySelectorAll(".no-js");
noJsElements.forEach((element) => {
  element.classList.remove("no-js");
});

mountVueApps();
