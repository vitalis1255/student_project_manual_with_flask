const button_upvote = document.querySelector('.js-upvote');
button_upvote.addEventListener('click', () =>{
  button_upvote.classList.toggle('active');
});

const button_downvote = document.querySelector('.js-downvote');
button_downvote.addEventListener('click', () =>{
  button_downvote.classList.toggle('active');
});

