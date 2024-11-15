// ! EM DESENVOLVIMENTO

function markAsSeen(){
    fetch("markAsSeen", {
        method: "POST"
    }).then(response => {
        console.log(response)
    })
}