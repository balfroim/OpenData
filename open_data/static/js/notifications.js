const list = document.querySelector('#notification-list')
const popup = document.querySelector('#notification-popup')
const counter = document.querySelector('#notification-count')

const queue = []

setInterval(pollNotifications, 3000)
popup.addEventListener('animationend', updatePopup)

async function pollNotifications() {
  const json = await fetch('/inbox/notifications/api/unread_list/?mark_as_read=true')
  const response = await json.json()

  const count = parseInt(counter.textContent)
  counter.textContent = `${count + response.unread_list.length}`

  for (const notification of response.unread_list) {
    const element = document.createElement('div')
    element.className = 'notification'

    const image = document.createElement('img')
    image.src = notification.data.image

    const description = document.createElement('div')
    description.textContent = notification.verb

    // Popup
    element.append(image)
    element.append(description)
    queue.push(element.cloneNode(true))
    updatePopup()

    // List
    element.classList.add('card')
    list.prepend(element)
  }
}

function updatePopup() {
  setTimeout(() => {
    if (!popup.classList.contains('active')) {
      const element = queue.shift()
      if (element !== undefined) {
        popup.innerHTML = ''
        popup.append(element)
        popup.classList.add('active')
      }
    }
  }, 200)
}
