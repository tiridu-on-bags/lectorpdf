import { browser } from '$app/environment';

export const ssr = false;

export const load = () => {
  let theme = null;
  if (browser) {
    theme = localStorage.getItem('theme');
  }
  return { theme };
};

