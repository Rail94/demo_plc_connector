/*

    L E T T U R A   S C R I T T U R A

*/

function getReadWrite(index, group_id){
    var urlBaseGetRW = "{{ url_for('logiche_blueprint.get_RW', group_id='__group_id__', RW = '__RW__') }}";
    var RW_select = this.previousElementSibling;
    const RW = RW_select.value;
    const urlWithGroupID = urlBaseGetRW.replace('__group_id__', group_id);
    urlWithGroupID = urlWithGroupID.replace('__RW__', RW);
    fetch(urlWithGroupID)
    .then(response => response.json())
        .then(data => {
            if(data.error) {
                console.error(data.error);
                return; // Gestisci l'errore come preferisci
            }
        
            this.innerHTML = ''; // Pulisci la select
            data.tipi.forEach(tipo => {
                var optionElement = document.createElement("option");
                optionElement.value = tipo.value;
                optionElement.textContent = tipo.key;
                this.appendChild(optionElement);
            });
        
            // Aggiorna l'oggetto tipiInfo con i nuovi tipi ricevuti
            tipiInfo = {};
            data.tipi.forEach(tipo => {
                tipiInfo[tipo.id] = { 'lettura': tipo.lettura, 'scrittura': tipo.scrittura };
            }); 

        })
        .catch(error => console.error('Errore nel recupero delle Tipologie di variabili dalla Marca PLC:', error));
}


/*

    C A R A T T E R I S T I C H E

*/

function getCaratteristiche(urlBaseGetCaratteristiche) {
    const marcaId = selectMarca.value;
    const urlWithMarcaId = urlBaseGetCaratteristiche.replace('__marca_id__', marcaId);
    
    fetch(urlWithMarcaId)
        .then(response => response.json())
        .then(data => {
            containerCaratteristiche.innerHTML = '';  // Pulisci il contenitore
            data.caratteristiche.forEach(caratteristica => {
                const div = document.createElement('div');
                div.className = 'mse-input-wrap';
                const label = document.createElement('label');
                label.className = 'mse-input-label';
                label.textContent = caratteristica + ':';
                const input = document.createElement('input');
                input.type = 'text';
                input.name = 'caratteristiche';
                input.placeholder = `Inserisci ${caratteristica}`;
                input.className = 'mse-input';
                div.appendChild(label);
                div.appendChild(input);
                containerCaratteristiche.appendChild(div);
            });
        })
    .catch(error => console.error('Errore nel recupero delle caratteristiche:', error));
}