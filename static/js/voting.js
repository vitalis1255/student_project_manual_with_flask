function UpvoteAndDownvote () {
  const up = document.querySelector('.js-upvote');
  const down = document.querySelector('.js-downvote');

  up.addEventListener('click', ()=>{
    up.classList.add();
    down.classList.remove()
  })
  down.addEventListener('click', ()=>{
    up.classList.remove();
    down.classList.add();
  })

}
UpvoteAndDownvote()