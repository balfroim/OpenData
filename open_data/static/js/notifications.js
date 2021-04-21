'use strict';

function fill_notifications_dropdown(data) {
  const notificationPopup = document.querySelector('#badge-popup');
  const notificationDropdown = document.querySelector('.live_notify_list');

  for (const notification of data.unread_list) {
    const description = document.createElement('span');
    const image = document.createElement('img');
    description.textContent = notification.verb;
    image.src = `/static/images/badges/${notification.data.image}`;
    image.width = 32;
    image.style = 'margin-right: 16px;';

    const element = document.createElement('div');
    element.style = 'display: flex; align-items: center;';
    element.appendChild(image);
    element.appendChild(description);

    notificationPopup.innerHTML = element.outerHTML;
    notificationPopup.classList.add('active');

    notificationDropdown.innerHTML = element.outerHTML;
  }
}
