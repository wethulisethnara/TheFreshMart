document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from refreshing the page
  
    // Get username and password entered by the user
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
  
    // Simple check for username and password (You can change these to whatever you like)
    if (username === "user" && password === "userpass") {
      // Redirect to the User page
      window.location.href = "userPage.html"; 
    } else if (username === "cashier" && password === "cashierpass") {
      // Redirect to the Cashier page
      window.location.href = "cashierPage.html";
    } else {
      alert("Invalid username or password");
    }
  });
  