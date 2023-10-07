document.addEventListener("DOMContentLoaded", function () {
    const convertBtn = document.getElementById("convertBtn");
    const inputTemp = document.getElementById("inputTemp");
    const fromUnit = document.getElementById("fromUnit");
    const toUnit = document.getElementById("toUnit");
    const result = document.getElementById("result");

    convertBtn.addEventListener("click", function () {
        const inputValue = parseFloat(inputTemp.value);
        if (isNaN(inputValue)) {
            result.textContent = "Please enter a valid temperature.";
            return;
        }

        const from = fromUnit.value;
        const to = toUnit.value;

        if (from === to) {
            result.textContent = "Result: " + inputValue + " " + from;
            return;
        }

        let convertedValue;

        if (from === "celsius" && to === "fahrenheit") {
            convertedValue = (inputValue * 9/5) + 32;
        } else if (from === "fahrenheit" && to === "celsius") {
            convertedValue = (inputValue - 32) * 5/9;
        } else if (from === "celsius" && to === "kelvin") {
            convertedValue = inputValue + 273.15;
        } else if (from === "kelvin" && to === "celsius") {
            convertedValue = inputValue - 273.15;
        } else if (from === "fahrenheit" && to === "kelvin") {
            convertedValue = (inputValue - 32) * 5/9 + 273.15;
        } else if (from === "kelvin" && to === "fahrenheit") {
            convertedValue = (inputValue - 273.15) * 9/5 + 32;
        }

        result.textContent = "Result: " + convertedValue.toFixed(2) + " " + to;
    });
});
