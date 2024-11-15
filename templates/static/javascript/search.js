const SEARCH_BAR = document.querySelector('#search_bar')

const RESULT_LIST = document.querySelector('.resultList')

async function search(){
    let input = SEARCH_BAR.value

    if (input == '') return


    const CATEGORY_OPTION = document.querySelector('input[name="category"]:checked')

    
    // let res = await fetch(`https://api.tvmaze.com/search/shows?q=${input}`).then((x) => x.json())
    let url = ''

    switch(CATEGORY_OPTION.value){
        // case 'all':
        //     url = `https://api.themoviedb.org/3/search/multi?query=${input}&include_adult=false&language=pt-BR&page=1`
        case 'movie':
            url = `https://api.themoviedb.org/3/search/movie?query=${input}&include_adult=false&language=pt-BR&page=1`
            break
        case 'serie':
            url = `https://api.themoviedb.org/3/search/tv?query=${input}&include_adult=false&language=pt-BR&page=1`
            break
        case 'anime':
            url = `https://api.themoviedb.org/3/search/tv?query=${input}&include_adult=false&language=pt-BR&page=1`
            break
        case 'game':
            url = ``
            break
        case 'book':
            url = ``
            break
        case 'user':
            url = ``
            break
    }
    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTEyYmNkYzc1ODMwOWFlZjU2YWI3YTFmYmQ3YzIyOCIsIm5iZiI6MTcyOTUxODIzMy41ODU4NTMsInN1YiI6IjY3MTNjMjM1ZDViNzkyNmU5NDZmYzQ5NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iPRn6COPbdHZ0BgkJ4hGeRZUjSrPVWGg-dfYs7ejka0'
        }
    }
    console.log(url)

    let res = await fetch(url, options).then(x => x.json()).catch(err => console.error(err))


    renderResult(resResolver(res), CATEGORY_OPTION.value)
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

function resResolver(origin){
    res = origin.results
    console.log(res)
    return res
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
            if (category == 'anime' && media.origin_country[0] != 'JP') continue
            if (category == 'serie' && media.origin_country[0] == 'JP') continue
            empty = false
            resultHTML += `
            <a href="/media?id=${media.id}&category=${category}" class="resultItem">
                ${fixImage(media)}
                <div class="searchMediaText">
                    <div class="mediaHeader">
                        <div class="mediaTitle">${solveMediaName(media)} <span class="time">${fixDate(media)}</span></div>
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


function solveMediaName(media){
    if (media.media_type){
        switch(media.media_type){
            case 'movie':
                return media.title
            case 'tv':
                return media.name
        }

    } else {
        if (media.title){
            return media.title
        }
        return media.name
    }
}


function fixDate(media){
    if (media.first_air_date != null){
        if (media.status == "Ended"){
            return `(${media.first_air_date.slice(0, 4)}-${media.ended.slice(0, 4)})`
        } else {
            return `(${media.first_air_date.slice(0, 4)})`
        }
    }
    return ''
}

function fixImage(media){

    if (media.poster_path != null){
        return `<img src="https://image.tmdb.org/t/p/w300_and_h450_bestv2${media.poster_path}" alt="" class="searchMediaImage"></img>`
    } else {
        return '<div class="theresNoImage">Sem imagem</div>'
    }

    // <img src="${media.image.medium}" alt="" class="searchMediaImage"></img>
}

function fixDescription(media){
    if (media.overview) {
        MAX_DESC_LENGTH = window.innerWidth > 960 ? 200 : 100
        // description = media.overview.slice(3, -4)
        description = media.overview
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