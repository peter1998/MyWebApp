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

function generateCaptcha() {
  const captchaDiv = document.getElementById("captchaDiv");
  const captchaChars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let captcha = "";
  for (let i = 0; i < 6; i++) {
    captcha += captchaChars.charAt(
      Math.floor(Math.random() * captchaChars.length)
    );
  }
  captchaDiv.textContent = captcha;
}

document.addEventListener("DOMContentLoaded", function () {
  generateCaptcha();
  const registerForm = document.getElementById("registerForm");

  registerForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const captchaInput = document.getElementById("captchaInput").value;

    if (
      !isValidEmail(email) ||
      !isValidName(name) ||
      !isValidPassword(password)
    ) {
      alert("Invalid input data or CAPTCHA.");
      return;
    }

    const formData = {
      email: email,
      name: name,
      password: password,
      captcha: captchaInput,
    };

    fetch("http://localhost:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Registration successful!");
          displayUserProfile(data.user);
        } else {
          alert("Registration failed. Please try again.");
          generateCaptcha();
        }
      })
      .catch((err) => {
        console.error("Error occurred:", err);
        alert("An error occurred. Please try again.");
        generateCaptcha();
      });
  });

  document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      console.log("Login Email:", email);
      console.log("Login Password:", password);

      fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      })
        .then((response) => {
          console.log("Login Response:", response);
          return response.json();
        })
        .then((data) => {
          console.log("Login data:", data);
          if (data.success && data.message === "Successful login!") {
            displayUserProfile(data.user);
          } else {
            alert("Login failed. Please check your credentials and try again.");
          }
        })
        .catch((err) => {
          console.error("Error occurred:", err);
          alert("An error occurred during login. Please try again.");
        });
    });

  function displayUserProfile(user) {
    if (!user || typeof user !== "object" || !user.email || !user.name) {
      console.error("Invalid user object:", user);
      return;
    }

    document.getElementById("registration").style.display = "none";
    document.getElementById("login").style.display = "none";
    const userProfile = document.getElementById("userProfile");
    document.getElementById("profileEmail").innerText = user.email;
    document.getElementById("profileName").innerText = user.name;
    userProfile.style.display = "block";
  }

  document
    .getElementById("editProfileForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const name = document.getElementById("editName").value;
      const password = document.getElementById("editPassword").value;

      fetch("http://localhost:8000/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: document.getElementById("profileEmail").innerText,
          name: name,
          password: password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success && data.user) {
            alert("User data updated successfully");
            displayUserProfile(data.user);
          } else {
            alert("Failed to update user data.");
          }
        })
        .catch((err) => {
          console.error("Error occurred:", err);
          alert("An error occurred during updating. Please try again.");
        });
    });

  document
    .getElementById("deleteProfileBtn")
    .addEventListener("click", function () {
      const email = document.getElementById("profileEmail").innerText;

      fetch("http://localhost:8000/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert("User deleted successfully");
            document.getElementById("userProfile").style.display = "none";
            document.getElementById("registration").style.display = "block";
            document.getElementById("login").style.display = "block";
          } else {
            alert("Failed to delete user.");
          }
        })
        .catch((err) => {
          console.error("Error occurred:", err);
          alert("An error occurred during deletion. Please try again.");
        });
    });

  function logout() {
    document.getElementById("userProfile").style.display = "none";
    document.getElementById("registration").style.display = "block";
    document.getElementById("login").style.display = "block";
    alert("Logged out successfully");
  }
});
