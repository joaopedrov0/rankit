let followBtn = document.querySelector(".followBtn")
let followersCounter = document.querySelector(".followers")

function follow(){
    followBtn.innerText = "Unfollow"
    followBtn.onclick = () => {unfollow()}

    fetch('follow')

    followersCounter.innerText = parseInt(followersCounter.innerText) + 1
}

function unfollow(){
    followBtn.innerText = "Follow"
    followBtn.onclick = () => {follow()}

    fetch('unfollow')

    followersCounter.innerText = parseInt(followersCounter.innerText) - 1
}