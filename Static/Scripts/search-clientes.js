// When the "Buscar" button is clicked
  document.getElementById("search-button").addEventListener("click", function () {
    // Get the customer code from the form
    var codigo = document.getElementById("search-codigo").value;
    
    // Make a GET request to the search endpoint with the code parameter
    fetch('/search?codigo=' + codigo)
    .then(response => response.json())
    .then(data => {
      if (Object.keys(data).length === 0) {
        // Show an error modal if the customer is not found
        var errorModal = new bootstrap.Modal(document.getElementById("error-modal"));
        errorModal.show();
      } else {
        // Fill out the modal with the customer data
        document.getElementById("username-1").value = data.nombre;
        document.getElementById("username-2").value = data.credito;
        // Show the modal
        var modal = new bootstrap.Modal(document.getElementById("modal-1"));
        modal.show();
      }
    })
    .catch(error => {
      console.error('Error:', error);
      // Display an error message in an alert
      alert(error);
    });
  });