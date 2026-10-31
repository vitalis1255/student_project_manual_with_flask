document.addEventListener("DOMContentLoaded", ()=>{
  const questionElement = document.getElementById("question-app");
  if(!questionElement) return;

  //Reading JSON safely from the script tag text content in question.html
  const questionsScript = document.getElementById("question-data");
  const questions = JSON.parse(questionsScript.textContent);
});