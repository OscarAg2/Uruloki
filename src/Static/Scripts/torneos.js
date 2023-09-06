const selectedOptions = [];

  function updateSelectedOptions() {
    const selectedOptionsText = selectedOptions.join(", ");
    const selectedOptionsElement = document.getElementById("selectedOptions");
    selectedOptionsElement.textContent = selectedOptionsText;
  }

  function resetFilters() {
    selectedOptions.length = 0;
    updateSelectedOptions();
  }

  document.querySelectorAll(".dropdown-menu a").forEach((item) => {
    item.addEventListener("click", (event) => {
      const optionValue = event.target.getAttribute("data-value");
      if (!selectedOptions.includes(optionValue)) {
        selectedOptions.push(optionValue);
        updateSelectedOptions();
      }
    });
  });

  document.getElementById("resetFiltersBtn").addEventListener("click", resetFilters);