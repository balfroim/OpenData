'use strict';

function fill_notifications_dropdown(data) {
  for (const list of document.getElementsByClassName('live_notify_list')) {
    list.textContent = '';
    for (const notification of data.unread_list) {
      const image = document.createElement('img');
      image.src = `/static/images/badges/${notification.data.image}`;
      const child = document.createElement('li');
      child.textContent = notification.verb;
      child.appendChild(image)
      list.appendChild(child);
    }
  }
}
