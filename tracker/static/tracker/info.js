document.addEventListener('DOMContentLoaded', () => {
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

    
    let count = 0;

    const checkDivs = document.getElementsByClassName('form-check');
    console.log(checkDivs);
    Array.from(checkDivs).forEach(div => {
        const checkbox = div.children[0];
        const list_id = div.children[1].id;
        
        console.log(checkbox);

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
        

        // https://stackoverflow.com/questions/6358673/javascript-checkbox-onchange used for checking the state of a checkbox
        checkbox.addEventListener('change', (event) => {
            if (event.currentTarget.checked) {
                alert('test');

                const options = {
                    method: 'GET',
                    headers: {
                    accept: 'application/json',
                    Authorization: `Bearer ${confid.TMDB_TOKEN}`
                    }
                };
                
                fetch(`https://api.themoviedb.org/3/${mediaType}/${id}?language=en-US`, options)
                .then(response => response.json())
                .then(response => {
                    console.log(response);

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
                alert('ah');
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
