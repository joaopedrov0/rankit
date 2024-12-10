const formHTML = document.querySelector("form")
const watchedHTML = document.querySelector(".interact .watched.btn")
const watchlistHTML = document.querySelector(".interact .watchList.btn")

formHTML.addEventListener('submit', (e) => {
    e.preventDefault()
    formHTML.submit()
    let select = document.querySelector('select')
    let textarea = document.querySelector('textarea')
    toggleFormModal()
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

function addWatchlist(){
    watchlistHTML.innerHTML = "Remover da watchlist"
    watchlistHTML.onclick = ()=>{removeWatchlist()}
    fetch(`/watchlist/${MEDIA_CATEGORY}/${MEDIA_ID}`, {method:"POST"})
}

function removeWatchlist(){
    watchlistHTML.innerHTML = "Adicionar a watchlist"
    watchlistHTML.onclick = ()=>{addWatchlist()}
    fetch(`/watchlist/${MEDIA_CATEGORY}/${MEDIA_ID}`, {method:"POST"})
}