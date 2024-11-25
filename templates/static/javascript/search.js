const SEARCH_BAR = document.querySelector('#search_bar')

const RESULT_LIST = document.querySelector('.resultList')

async function search(){
    let input = SEARCH_BAR.value

    if (input == '') return


    const CATEGORY_OPTION = document.querySelector('input[name="category"]:checked')

    
    // let res = await fetch(`https://api.tvmaze.com/search/shows?q=${input}`).then((x) => x.json())
    let url = `/searchMedia/${CATEGORY_OPTION.value}/${input}`


    console.log(url)

    let headers = {
        method: "GET"
    }

    let res = await fetch(url, headers).then(x => x.json()).catch(err => console.error(err))

    console.log(res)

    renderResult(res.result, CATEGORY_OPTION.value)
}



const CATEGORY_FILTER = document.querySelectorAll(".category > *")
function cleanFilter(){
    for(i in CATEGORY_FILTER){
        console.log(CATEGORY_FILTER[i])
        console.log(CATEGORY_FILTER)
        if (CATEGORY_FILTER[i].classList.contains("selected")){
            
            CATEGORY_FILTER[i].classList.remove("selected")
        }
    }
}

const titleHTML = document.querySelector('title')

function renderResult(res, category){
    console.log(res)
    titleHTML.innerText = `Buscando resultados para "${SEARCH_BAR.value}" - rank.it`
    resultHTML = `<h2>Exibindo resultados para "${SEARCH_BAR.value}"</h2>`
    let empty = true
    if (res.length != 0){
        for (i in res){
            media = res[i]
            empty = false
            resultHTML += `
            <a href="/media?id=${media.id}&category=${media.category}" class="resultItem">
                ${fixImage(media)}
                <div class="searchMediaText">
                    <div class="mediaHeader">
                        <div class="mediaTitle">${media.title} <span class="time">${fixDate(media)}</span></div>
                        <div class="score"><span class="stars">⭐⭐⭐⭐⭐</span> | <span class="views">6.9k</span> views</div>
                    </div>
                    
                    <div class="mediaDescription">${fixDescription(media)}</div>
                </div>
            </a>`
        }
    
        
    }
    if (empty){
        resultHTML += `<p class="notFound">Oops, não encontrei o que você está buscando. Verifique a ortografia!</p>`
    }
    RESULT_LIST.innerHTML = resultHTML 
}



function fixDate(media){
    if (media.release_date != null){
        return `(${media.release_date.slice(0, 4)})`
    }
    return ''
}

function fixImage(media){

    if (media.poster_path){
        return `<img src="${media.poster_path}" alt="" class="searchMediaImage"></img>`
    } else {
        return '<div class="theresNoImage">Sem imagem</div>'
    }

    // <img src="${media.image.medium}" alt="" class="searchMediaImage"></img>
}

function fixDescription(media){
    if (media.description) {
        MAX_DESC_LENGTH = window.innerWidth > 960 ? 200 : 100
        // description = media.overview.slice(3, -4)
        description = media.description
        if (description.length > MAX_DESC_LENGTH){
            description = description.slice(0, MAX_DESC_LENGTH)
            description = description.split(' ')
            description.pop()
            description = description.join(' ')
            description += ' [...]'
        }
        return description
    } else {
        return '[No description]'
    }
}

function checkEnter(e){
    if(e.code == 'Enter'){
        search()
    }
}