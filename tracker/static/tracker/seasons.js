document.addEventListener('DOMContentLoaded', () => {
    // Get id of media
    const path = window.location.pathname;
    const mediaId = path.slice(4, path.lastIndexOf('/'));
    
    // Display season 1 information
    document.getElementById('season1').style.display = 'block';
    const buttons = document.getElementsByClassName('buttons');
    Array.from(buttons).forEach(button => {
        // Get data for each season and its episodes
        const options = {
            method: 'GET',
            headers: {
            accept: 'application/json',
            Authorization: `Bearer ${confid.TMDB_TOKEN}`
            }
        };
        
        fetch(`https://api.themoviedb.org/3/tv/${mediaId}/season/${button.id}?language=en-US`, options)
            .then(response => response.json())
            .then(response => {
                const info = document.getElementById(`acc${button.id}`);
                response.episodes.forEach(episode => {
                    info.innerHTML += `
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse${episode.episode_number}" aria-expanded="false" aria-controls="flush-collapseOne">
                                <b style='margin-right: 8px;'>${episode.episode_number}.</b><span> ${episode.name}</span>
                            </button>
                        </h2>
                        <div id="flush-collapse${episode.episode_number}" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div class="accordion-body">
                                ${episode.overview}
                                <hr/>
                                <dl class="row">
                                <dt class="col-sm-2">Air date: </dt>
                                <dd class="col-sm-10">${episode.air_date}</dd>
                                <dt class="col-sm-2">Runtime: </dt>
                                <dd class="col-sm-10">${episode.runtime} minutes</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                    `;  
                });
            })
            .catch(err => console.error(err));
        
        // Display season info when button clicked and hide other seasons
        button.addEventListener('click', () => {
            const seasons = document.getElementsByClassName('season_div');
            Array.from(seasons).forEach(div => {
                div.style.display = 'none';
            });
            let season = document.getElementById(`season${button.id}`);
            season.style.display = 'block';
        });   
    });
});