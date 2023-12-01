document.getElementById("update-button").addEventListener("click", function () {
    // Get the customer code, name, and credit from the form
    var codigo = document.getElementById("search-codigo").value;
    var nombre = document.getElementById("username-1").value;
    var credito = document.getElementById("username-2").value;
  
    // Make a PUT request to the update endpoint with the code parameter
    fetch('/update?codigo=' + codigo, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'nombre=' + encodeURIComponent(nombre) + '&credito=' + encodeURIComponent(credito)
    })
    .then(response => response.json())
    .then(data => {
      // Display a success or error message in an alert
      alert(data.message);
      // Hide the modal
      var modal = new bootstrap.Modal(document.getElementById("modal-1"));
      modal.hide();
    })
    .catch(error => {
      console.error('Error:', error);
      // Display an error message in an alert
      alert('An error occurred while updating the customer data');
    });
  });