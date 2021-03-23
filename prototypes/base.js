'use strict';

// Define custom elements
for (const template of document.getElementsByTagName('template')) {
  customElements.define(template.id, 
    class extends HTMLElement {
      constructor() {
        super();
        this.attachShadow({ mode: 'open' })
          .appendChild(template.content.cloneNode(true));
      }
    }
  )
}

// Fade elements
let i = 1;
for (const node of document.getElementsByClassName('fading')) {
  node.classList.add('fading-start')
  setTimeout(() => node.classList.remove('fading-start'), i++ * 120);
}
