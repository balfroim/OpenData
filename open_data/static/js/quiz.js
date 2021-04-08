'use strict';

for (const form of document.getElementsByClassName('quiz-form')) {
  const id = form.dataset.quizId;
  form.addEventListener('submit', async event => {
    event.preventDefault();

    const response = await fetch(`/quiz/${id}/`, {
      method: 'POST',
      body: new URLSearchParams(new FormData(form)),
    });

    const html = await response.text();
    form.parentElement.outerHTML = html;
  });
}
