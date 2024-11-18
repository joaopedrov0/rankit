// ! EM DESENVOLVIMENTO

document.querySelector("button[type='submit']").addEventListener('submit', (e) => {
    e.preventDefault()
    
})

function toggleFormModal(){

}

function markAsSeen(){
        fetch(`markAsSeen/${MEDIA_CATEGORY}/${MEDIA_ID}`, {
        method: "POST",
        teste: "testado fi"
    }).then(response => {
        res = response.headers.get("request-status")
        if (res == "Accepted"){
            alert("Adicionado com sucesso")
        } else{
            alert(`Recusado. Motivo: ${res}`)
        }
    })
}


// MUDANÇA DE ESTRATEGIA >>> VAI SER UM FORMULARIO

