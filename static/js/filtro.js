let inputFiltro = document.getElementById('input-filtro');
let arrayCards = document.getElementsByClassName('card');

function filtrar(){
    // Valor a buscar
    const valueFiltro = inputFiltro.value.toLowerCase();
    // Buscar entre todas las tarjetas de noticias
    for (let i=0;i<arrayCards.length;i++){
        // Tarjeta
        let card = arrayCards[i]
        // Iterar sobre el body de la tarjeta
        const hijosCard = arrayCards[i].children[0];
        // Sacar el titulo y descripcion
        const titulo = hijosCard.children[0].innerText.toLowerCase();
        const descripcion = hijosCard.children[1].innerText.toLowerCase();
        if (!titulo.includes(valueFiltro)){
            card.style.display = "none";
        }else{
            console.log('No incluye')
            card.style.display = "block"
        }
    }
}

inputFiltro.addEventListener('keyup',filtrar)