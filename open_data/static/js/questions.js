const form = document.querySelector('#add-question-form');
const list = document.querySelector('#questions-list');
const url = form.dataset.url;

form.addEventListener('submit', async event => {
  event.preventDefault()

  const response = await fetch(url, {
    method: 'POST',
    body: new URLSearchParams(new FormData(form)),
  })

  if (response.ok) {
    list.innerHTML = await response.text()
  } else {
    list.innerHTML = '<div class="card"><p>Une erreur est survenue.</p></div>'
  }
})
