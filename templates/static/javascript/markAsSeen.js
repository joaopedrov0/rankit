// ! EM DESENVOLVIMENTO

const formHTML = document.querySelector("form")
const watchedHTML = document.querySelector(".interact .watched.btn")

formHTML.addEventListener('submit', (e) => {
    e.preventDefault()
    formHTML.submit()
    let select = document.querySelector('select')
    let textarea = document.querySelector('textarea')

    // select.value = ''
    // textarea.value = ''
    toggleFormModal()
    // watchedHTML.disabled = true
    // watchedHTML.onclick = null
    watchedHTML.innerHTML = "Editar review <span class='material-symbols-outlined filled'>edit</span>"
})

document.querySelector('form').action = `${location.origin}/markAsSeen/${MEDIA_CATEGORY}/${MEDIA_ID}`

function toggleFormModal(){
    const model = document.querySelector('.modal-blocker')
    model.classList.toggle('hidden')
}

function removeView(){
    toggleFormModal()
    watchedHTML.innerHTML = "Marcar como visto"
    fetch(`/removeAsSeen/${MEDIA_CATEGORY}/${MEDIA_ID}`, {method:"POST"})
}

// function markAsSeen(){
//         fetch(`markAsSeen/${MEDIA_CATEGORY}/${MEDIA_ID}`, {
//         method: "POST",
//         teste: "testado fi"
//     }).then(response => {
//         res = response.headers.get("request-status")
//         if (res == "Accepted"){
//             alert("Adicionado com sucesso")
//         } else{
//             alert(`Recusado. Motivo: ${res}`)
//         }
//     })
// }


// MUDANÇA DE ESTRATEGIA >>> VAI SER UM FORMULARIO

