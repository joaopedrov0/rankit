function registerIcon(value){
    target = document.querySelector(`#icon-${value}`)
    selected = document.querySelector(".icon-option.option-selected")
    if (selected){
        selected.classList.toggle("option-selected")
    }
    target.classList.toggle("option-selected")
    input = document.querySelector("#icon-input")
    input.value = value
}

function registerBanner(value){
    target = document.querySelector(`#banner-${value}`)
    selected = document.querySelector(".banner-option.option-selected")
    if (selected){
        selected.classList.toggle("option-selected")
    }
    target.classList.toggle("option-selected")
    input = document.querySelector("#banner-input")
    input.value = value
}