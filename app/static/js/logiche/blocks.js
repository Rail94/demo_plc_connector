

function aggiungiBloccoDelay(delay_counter) {

    var main = document.getElementById("logiche");

    var options = [
        { value: "", text: "--Seleziona--"},
        { value: "s", text: "Secondo/i"},
        { value: "m", text: "Minuto/i"},
        { value: "h", text: "Ora/e"}
    ]

    var divParent = document.createElement("div");
    divParent.className = "mse-input-row-wrap";
    
    var divChild1 = document.createElement("div");
    divChild1.className = "mse-input-wrap";

    var label_input = LabelforSelectConstructor("mse-input-label", "delay_input", "Unità di misura");
    var input = InputConstructor("mse-input", "delay_" + delay_counter, "delay_input", "text", "Valore...")
    
    divChild1.append(label_input, input);



    var divChild2 = document.createElement("div");
    divChild2.className = "mse-input-wrap";
    
    var label_select = LabelforSelectConstructor("mse-input-label", "delay_measure", "Unità di misura");
    var select = SelectElementConstructor("mse-input", "delay_measure", "delay_" + delay_counter, "", options);
    
    divChild2.append(label_select, select);

    // Bottone di eliminazione del blocco
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        divParent.remove();
    };

    divParent.appendChild(divChild1, divChild2, deleteButton)

    main.appendChild(divParent)
}


function aggiungiBloccoCondizione(condition_counter) {

    var main = document.getElementById("logiche");

    var options = [
        { value: "R", text: "Lettura"},
        { value: "W", text: "Scrittura"}
    ]

    var divParent = document.createElement("div");
    divParent.className = "mse-input-row-wrap";
    divParent.id = "conditionBlock_" + condition_counter; 

    // Costruttore per il "div" che contiene la "select" e la sua "label"
    function createChildDiv(labelFor, selectNameId, labelText, functionGet, options) {
        var divChild = document.createElement("div");
        divChild.className = "mse-input-wrap";
        
        var label = LabelforSelectConstructor("mse-input-label", labelFor, labelText);
        var select = SelectElementConstructor("mse-input", selectNameId, selectNameId, functionGet, options);

        divChild.append(label, select);
        return divChild;
    }

    var divChild1 = createChildDiv("condition_RW1", "condition_RW1", "Tipo", "",options);
    var divChild2 = createChildDiv("condition_Var1", "conditionVar1", "Variabile", function() { getReadWrite(1); }, "");
    var divChild3 = createChildDiv("condition_RW2", "condition_RW2", "Tipo", "", options);
    var divChild4 = createChildDiv("condition_Var2", "condition_Var2", "Variabile",  function() { getReadWrite(2); }, "");

    // Bottone di eliminazione del blocco
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        divParent.remove();
    };
    divParent.append(divChild1, divChild2, divChild3, divChild4, deleteButton);
    main.appendChild(divParent);
}