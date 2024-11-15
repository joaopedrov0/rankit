// ! EM DESENVOLVIMENTO

function markAsSeen(){
        fetch(`markAsSeen/${MEDIA_CATEGORY}/${MEDIA_ID}`, {
        method: "POST"
    }).then(response => {
        res = response.headers.get("request-status")
        if (res == "Accepted"){
            alert("Adicionado com sucesso")
        } else{
            alert(`Recusado. Motivo: ${res}`)
        }
    })
}

