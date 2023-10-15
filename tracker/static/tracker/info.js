document.addEventListener('DOMContentLoaded', () => {
    // Get id of media
    const path = window.location.pathname;
    const id = path.substring(path.lastIndexOf('/') + 1);

    let mediaType;
    if (path.includes('movies')) {
        mediaType = 'movie';
    } else if (path.includes('tv')) {
        mediaType = 'tv';
    }

    const errors = document.getElementsByClassName('errorlist');
    if (errors.length > 0) {
        errors[0].remove();
    }

    // Checks if item is on any lists and changes checkbox state
    const checkDivs = document.getElementsByClassName('form-check');
    let count = 0;
    Array.from(checkDivs).forEach(div => {
        const checkbox = div.children[0];
        const list_id = div.children[1].id;
        fetch(`/api/lists/${list_id}`)
        .then(response => response.json())
        .then(response => {
            response.media.forEach(item => {
                if(mediaType == item.type && item.data.id == id) {
                    checkbox.checked = true;
                    count+=1;
                }
            });
        })

        // Code from https://stackoverflow.com/questions/6358673/javascript-checkbox-onchange used for checking the state of a checkbox
        checkbox.addEventListener('change', (event) => {
            if (event.currentTarget.checked) {
                const options = {
                    method: 'GET',
                    headers: {
                    accept: 'application/json',
                    Authorization: `Bearer ${confid.TMDB_TOKEN}`
                    }
                };
                
                // Get media object from TMDB
                fetch(`https://api.themoviedb.org/3/${mediaType}/${id}?language=en-US`, options)
                .then(response => response.json())
                .then(response => {
                    // Creates media object to be stored in the database
                    fetch(`/api/media/${mediaType}/${id}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                        },
                        body: JSON.stringify({
                            obj_id: `${id}`,
                            mediaType: `${mediaType}`,
                            data: `${JSON.stringify(response)}`
                        })
                    });

                    // Adds media object to list
                    fetch(`/api/lists/${list_id}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                        },
                        body: JSON.stringify({
                            obj_id: `${id}`,
                            mediaType: `${mediaType}`,
                            action: 'add'
                        })
                    });

                })
                .catch(err => console.error(err));

            } else {
                // Removes media object from list
                fetch(`/api/lists/${list_id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    },
                    body: JSON.stringify({
                        obj_id: `${id}`,
                        mediaType: `${mediaType}`,
                        action: 'remove'
                    })
                });
            }
        });
    });

    // alert(count);

    // const listBadge = document.getElementById('list-count');
    // alert(listBadge.innerHTML);
    // listBadge.innerHTML = `Added to ${count} lists`;
});
