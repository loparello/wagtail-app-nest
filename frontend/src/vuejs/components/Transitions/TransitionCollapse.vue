<template>
  <transition
    name="collapse"
    @enter="onEnter"
    @leave="onLeave"
    @before-enter="beforeEnter"
    @before-leave="beforeLeave"
    @after-enter="onAfterEnter"
  >
    <slot></slot>
  </transition>
</template>

<script lang="ts" setup>
// Methods
const beforeEnter = (el: Element): void => {
  const element = el as HTMLElement;
  element.style.height = '0';
};

const onEnter = (el: Element): void => {
  const element = el as HTMLElement;
  element.style.height = element.scrollHeight + 'px';
};

const onAfterEnter = (el: Element): void => {
  const element = el as HTMLElement;
  element.style.height = 'auto';
};

const beforeLeave = (el: Element): void => {
  const element = el as HTMLElement;
  element.style.height = element.offsetHeight + 'px';
};

const onLeave = (el: Element): void => {
  const element = el as HTMLElement;
  element.style.height = '0';
};
</script>
