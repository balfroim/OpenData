'use strict';

// Display the modals when clicking on the log in button and hide them when
// clicking anywhere else

const button = document.querySelector('#modal-show');
const mask = document.querySelector('#modal-mask');

button.addEventListener('click', () => {
  mask.classList.add('active');
});

mask.addEventListener('click', e => {
  if (e.target === mask) {
    mask.classList.remove('active');
  }
});
