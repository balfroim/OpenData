'use strict';

// Make a fade-in transition for every elements in <main />

const main = document.querySelector('main');

let i = 1;
for (const child of main.children) {
  setTimeout(() => child.classList.add('fading'), i * 100);
  i += 1;
}
