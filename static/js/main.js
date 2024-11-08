var a;
function LoginPass() {
  if (a == 1) {
    document.getElementById("password").type = "password";
    document.getElementById("show-password").type = "checkbox";
    a = 0;
  } else {
    document.getElementById("password").type = "text";
    document.getElementById("show-password").type = "checkbox";
    a = 1;
  }
}

function RegisterPass() {
  if (a == 1) {
    document.getElementById("password").type = "password";
    document.getElementById("password").type = "password";
    document.getElementById("show-password").type = "checkbox";
    a = 0;
  } else {
    document.getElementById("password").type = "text";
    document.getElementById("password").type = "text";
    document.getElementById("show-password").type = "checkbox";
    a = 1;
  }
}

const numberInput = document.getElementById('numberInput');
const incrementBtn = document.getElementById('incrementBtn');
const decrementBtn = document.getElementById('decrementBtn');

  // Add click event listeners to the buttons
incrementBtn.addEventListener('click', () => {
  numberInput.stepUp();
});

decrementBtn.addEventListener('click', () => {
  numberInput.stepDown();
});