// Intro animation
let i = 1;
for (const element of document.querySelectorAll('main > *')) {
  setTimeout(() => { element.classList.add('fading'); }, i * 100);
  i += 1;
}

// Tabs
for (const parent of document.querySelectorAll('.tabs')) {
  const tabs = parent.querySelectorAll('.tab');
  for (const tab of tabs) {
    const buttons = document.querySelectorAll(`.${tab.id}-button`);
    if (buttons.length === 0) {
      console.warn(`The tab '#${tab.id}' has no corresponding '.${tab.id}-button'. It will thus never be displayed!`);
    } else for (const button of buttons) {
      button.addEventListener('click', () => {
        for (const other of tabs) {
          if (other === tab) {
            other.classList.add('active');
          } else {
            other.classList.remove('active');
          }
        }
      });
    }
  }
}

// Modals
const masks = document.querySelectorAll('.modal-mask');
for (const mask of masks) {
  mask.addEventListener('click', event => {
    if (event.target === mask) {
      mask.classList.remove('active');
    }
  });

  const buttons = document.querySelectorAll(`.${mask.id}-button`);
  if (buttons.length === 0) {
    console.warn(`The modal-mask '#${mask.id}' has no corresponding '.${mask.id}-button'. It will thus never be displayed!`);
  } else for (const button of buttons) {
    button.addEventListener('click', () => {
      mask.classList.toggle('active');
      for (const other of masks) {
        if (other !== mask) {
          other.classList.remove('active');
        }
      }
    });
  }
}

// Pop-ups
for (const element of document.querySelectorAll('.popup')) {
  element.addEventListener('animationend', () => {
    element.classList.remove('active');
  });
}

// Svg colors
for (const element of document.querySelectorAll('.svg')) {
  element.style.setProperty('--svg-src', `url(${element.dataset.src})`)
  element.style.setProperty('--svg-color', element.dataset.color)
}
