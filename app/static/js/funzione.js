 // Seleziona il bottone
 let scrollToTopBtn = document.getElementById("scrollToTopBtn");

 // Mostra il bottone quando l'utente scorre in basso di 20px dalla cima della pagina
 window.onscroll = function() {scrollFunction()};

 function scrollFunction() {
     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
         scrollToTopBtn.classList.remove("hidden");
     } else {
         scrollToTopBtn.classList.add("hidden");
     }
 }

 // Quando l'utente clicca sul bottone, scrolla verso l'alto della pagina
 scrollToTopBtn.onclick = function() {
     window.scrollTo({top: 0, behavior: 'smooth'});
 }





/* INIZO CARICAMENTO  DELLA PAGINA DI APERTURA HOME  */


// Simula il caricamento del tuo contenuto
document.addEventListener("DOMContentLoaded", function () {
    // Rimuovi la schermata di caricamento dopo un certo periodo di tempo (simulazione)
    setTimeout(function () {
        document.querySelector(".loader-container").style.display = "none";
    }, 3000); 
});

/* FINE CARICAMENTO  DELLA PAGINA DI APERTURA HOME */

function buttonFeedback(button) {
    button.style.backgroundColor = '#d0d0d0';
    setTimeout(function() {
        button.style.backgroundColor = '#f0f0f0';
    }, 200);
}
 /* per manu damobile */
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
  });
  
  document.getElementById('close-mobile-menu').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.add('hidden');
  });


  /* per le tabbelle */

  $(document).ready(function () {
    $("#deviceTable").DataTable();
  });
  
  $(document).ready(function () {
    $("#deviceTable").DataTabl();
  });


  function toggleLight(id) {
    // Spegne tutti i pallini
    for (let i = 1; i <= 5; i++) {
        document.getElementById('light' + i).classList.remove('light-on');
    }
    // Accende o spegne il pallino cliccato
    const light = document.getElementById('light' + id);
    if (!light.classList.contains('light-on')) {
        light.classList.add('light-on');
    } else {
        light.classList.remove('light-on');
    }
}


