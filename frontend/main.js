function isValidEmail(email) {
  let re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  return re.test(email);
}

function isValidName(name) {
  return name.trim().length > 0;
}

function isValidPassword(password) {
  let re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
  return re.test(password);
}

document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    if (!isValidEmail(email)) {
      alert("Invalid email format!");
      return;
    }

    if (!isValidName(name)) {
      alert("Name cannot be empty!");
      return;
    }

    if (!isValidPassword(password)) {
      alert(
        "Password should be at least 8 characters, contain at least one uppercase letter, one number, and one special character."
      );
      return;
    }

    fetch("http://localhost:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        name: name,
        password: password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Registration successful!");
        } else {
          alert("Registration failed. Please try again.");
        }
      })
      .catch((err) => {
        console.error("Error occurred:", err);
        alert("An error occurred. Please try again.");
      });
  });
