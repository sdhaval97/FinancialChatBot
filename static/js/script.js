document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        // Get input values
        const ageInput = document.getElementById("age").value.trim();
        const incomeInput = document.getElementById("income").value.trim();
        const expensesInput = document.getElementById("expenses").value.trim();

        // Validate age, income, and expenses fields
        if (!validateNumberInput(ageInput)) {
            alert("Please enter a valid age.");
            event.preventDefault();
        }

        if (!validateNumberInput(incomeInput)) {
            alert("Please enter a valid income.");
            event.preventDefault();
        }

        if (!validateNumberInput(expensesInput)) {
            alert("Please enter a valid expenses.");
            event.preventDefault();
        }
    });

    // Function to validate numeric inputs
    function validateNumberInput(value) {
        // Check if the value is a number and not empty
        return !isNaN(parseFloat(value)) && isFinite(value) && value !== "";
    }
});
