document.addEventListener('DOMContentLoaded', () => {
    const url = window.location.search;
    const param = new URLSearchParams(url);
    const q = param.get('q');
    
    if (q !== null) {
        displaySearchResults(q);
    } else if (param == '') {
        displayTrending();
    }
});

/**
 * Determines the type of media that is currently being searched for
 * @returns the media type in string form or null otherwise
 */
function getMediaType() {
    const searchbar = document.querySelector('input');
    if (searchbar.placeholder.includes('Movie')) {
        return 'movie';
    } else if (searchbar.placeholder.includes('TV')) {
        return 'tv';
    } else if (searchbar.placeholder.includes('Book')) {
        return 'book';
    }
    return null;
}

/**
 * Displays the search results for the desired query
 * @param {string} query The title of a book, tv show, or movie
 */
function displaySearchResults(query) {
    let mediaType = getMediaType();
    document.getElementById('icons').style.display = 'none';
    if (mediaType === 'tv' || mediaType === 'movie') {
        const options = {
            method: 'GET',
            headers: {
                accept: 'application/json',
                Authorization: `Bearer ${confid.TMDB_TOKEN}`
            }
        };

        const display = document.getElementById('display');
        display.innerHTML = "";
        
        fetch(`https://api.themoviedb.org/3/search/${mediaType}?query=${query}&include_adult=false&language=en-US&page=1`, options)
        .then(response => response.json())
        .then(response => {
            const message = document.getElementById('message');
            if (response.success === false) {
                display.setAttribute("class", "");
                message.innerHTML = 'There was an error generating your request.';
            }
            message.innerHTML = `<small><span class='lead'>${response.total_results} results for '${query}'<span></small>`

            loadItems(response);

            let currentPage = parseInt(response.page);
            const lastPage = parseInt(response.total_pages);
            document.addEventListener('scroll', () => {
                if (currentPage <= lastPage && window.innerHeight + window.scrollY > document.body.scrollHeight) {
                    currentPage++;
                    fetch(`https://api.themoviedb.org/3/search/${mediaType}?query=${query}&include_adult=false&language=en-US&page=${currentPage}`, options)
                    .then(newResponse => newResponse.json())
                    .then(newResponse => {
                        loadItems(newResponse);
                    });
                }
            });
            
        })
        .catch(err => console.error(err));
    } else if (mediaType === 'book') {
        alert('test');
        fetch(`https://openlibrary.org/search.json?q=${query}`)
        .then(response => response.json())
        .then(results => {
            // console.log(results);
            results.docs.forEach(element => {
                console.log(element.key)

                fetch(`https://openlibrary.org${element.key}.json`)
                .then(response => response.json())
                .then(book => {
                    console.log(book);
            
                })
                .catch(err => console.error(err));
            });
        });
    }
}

function displayTrending() {

}

/**
 * Helper method to display search results. 
 * @param {JSON} response all relevant info about the searched query
 */
function loadItems(response) {
    // console.log(response)
    response.results.forEach(element => {
        // console.log(element.title);
        const card = document.createElement('div');
        card.classList.add('card');
        card.classList.add('shadow-sm');
        card.classList.add('media');
        const link = document.createElement('a');
        link.href = `${window.location.pathname}/${element.id}`
        link.classList.add('link');
        card.appendChild(link);
        const img = document.createElement('img');
        if (element.poster_path !== null) {
            img.src = `https://image.tmdb.org/t/p/w185${element.poster_path}`;
            img.classList.add('card-img-top');
            img.alt = 'Poster';
            link.appendChild(img); 
        } else {
            link.innerHTML += `
            <div class="card" style="border-width: 0px;">
                <div class="card-body">
                    <p class="no-poster"><i>No Poster</i></p>
                </div>
            </div>`
        }
        
        if (getMediaType() === 'movie') {
            card.innerHTML += `
            <div class="card-body" style="padding: 0px;">
                <span class="badge text-bg-danger">Movie</span>
                <p class="card-text title"><small>${element.title}</small></p>
            </div>
            `
        } else if (getMediaType() === 'tv') {
            link.innerHTML += `
            <div class="card-body" style="padding: 0px;">
                <span class="badge text-bg-success">TV</span>
                <p class="card-text title"><small>${element.name}</small></p>
            </div>
            `
        }
        
        display.appendChild(card);
    });
}
