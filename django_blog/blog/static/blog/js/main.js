// static/blog/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(".alert");
  messages.forEach(function (message) {
    setTimeout(function () {
      message.style.opacity = "0";
      setTimeout(function () {
        message.style.display = "none";
      }, 300);
    }, 5000);
  });

  // Confirm before deleting posts
  const deleteButtons = document.querySelectorAll(".btn-danger");
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function (e) {
      if (!confirm("Are you sure you want to delete this post?")) {
        e.preventDefault();
      }
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach(function (field) {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = "#dc3545";

          // Create error message if not exists
          if (
            !field.nextElementSibling ||
            !field.nextElementSibling.classList.contains("error-message")
          ) {
            const errorMsg = document.createElement("div");
            errorMsg.className = "error-message";
            errorMsg.style.color = "#dc3545";
            errorMsg.style.fontSize = "0.875rem";
            errorMsg.style.marginTop = "5px";
            errorMsg.textContent = "This field is required";
            field.parentNode.appendChild(errorMsg);
          }
        } else {
          field.style.borderColor = "#28a745";
          const errorMsg = field.parentNode.querySelector(".error-message");
          if (errorMsg) {
            errorMsg.remove();
          }
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  });
});
