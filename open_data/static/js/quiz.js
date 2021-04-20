for (const form of document.getElementsByClassName('quiz-form')) {
  const id = form.dataset.quizId;
  form.addEventListener('submit', async event => {
    event.preventDefault();

    const response = await fetch(`/quiz/${id}/`, {
      method: 'POST',
      body: new URLSearchParams(new FormData(form)),
    });

    if (response.ok) {
      const html = await response.text();
      form.parentElement.outerHTML = html;
    } else {
      form.parentElement.innerHTML = '<div class="card"><p>Une erreur est survenue.</p></div>'
    }
  });
}
