/*

    COSTRUTTORI

*/
function LabelforSelectConstructor(className, for_label, textContent) {
    // Create the select element
    var label = document.createElement("select");

    // Set the properties
    label.className = className;
    label.setAttribute("for", for_label);
    label.textContent = textContent;
    // Return the created select element
    return label;
}

function InputConstructor(className, name, id, type, placeholder) {
    // Create the select element
    var input = document.createElement("input")

    // Set the properties
    input.className = className;
    input.type = type;
    input.name = name;
    input.id = id;
    input.placeholder = placeholder;

    // Return the created select element
    return input;
}

function SelectElementConstructor(className, id, name, onchangeFunction, options) {
    // Create the select element
    var select = document.createElement("select");

    // Set the properties
    select.className = className;
    select.name = name;
    select.id = id;

    // Check and assign the onchange event handler if it exists
    if (typeof onchangeFunction === 'function') {
        select.onchange = onchangeFunction;
    }

    // Add options to the select element
    if (options && options.length) {
        options.forEach(function (option) {
            var optionElement = document.createElement("option");
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            select.appendChild(optionElement);
        });
    }

    // Return the created select element
    return select;
}



