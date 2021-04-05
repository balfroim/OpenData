'use strict';

// Get every mask on the page.
// For instance:
//   <div id="a-mask" class="inactive mask" />
//   <div id="b-mask" class="inactive mask" />
// Makes an array:
//   [
//     ['a', <div ... />],
//     ['b', <div ... />],
//   ]
const masks = Array.from(document.getElementsByClassName('mask'))
  .map(element => [element.id.match(/^(.*)-mask$/)[1], element]);

for (const [id, element] of masks) {
  // Hide a mask when the user clicks on it.
  element.addEventListener('click', event => {
    if (event.target === element) {
      hideMask(element);
    }
  });

  // Display masks when asked.
  // For instance, a click on <div class="a-button" /> will display
  // <div class="a-mask /> and hide other masks.
  for (const button of document.getElementsByClassName(`${id}-button`)) {
    button.addEventListener('click', () => {
      toggleMask(element);
    });
  }
}

// Mask toggling
function toggleMask(element) {
  hideMasksExcept(element);
  const inactive = element.classList.toggle('inactive');

  // We use the following hack to remove page overflow for drop-downs.
  // TODO (non-urgent): find an alternative
  document.body.style = inactive ? '' : 'overflow: hidden;';
}

function hideMasksExcept(excepted) {
  for (const [, element] of masks) {
    if (element !== excepted) {
      element.classList.add('inactive');
    }
  }
}

function hideMask(element) {
  element.classList.add('inactive');
  document.body.style = ''; // see comment above
}
