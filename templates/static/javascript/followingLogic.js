let followBtn = document.querySelector(".followBtn")
let followersCounter = document.querySelector(".followers")

function follow(){
    followBtn.innerText = "Unfollow"
    followBtn.onclick = () => {unfollow()}

    // fetch('follow/', {method: 'POST'})

    followersCounter.innerText = parseInt(followersCounter.innerText) + 1

    revealSuggestions()
}

function unfollow(){
    followBtn.innerText = "Follow"
    followBtn.onclick = () => {follow()}

    // fetch('unfollow/', {method: 'POST'})

    followersCounter.innerText = parseInt(followersCounter.innerText) - 1
}
