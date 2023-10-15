document.addEventListener('DOMContentLoaded', () => {
    // Force reload to update HTML from https://stackoverflow.com/questions/43043113/how-to-force-reloading-a-page-when-using-browser-back-button
    var perfEntries = performance.getEntriesByType("navigation");
    if (perfEntries[0].type === "back_forward") {
        location.reload();
    }

    const delButton = document.getElementById('delete');
    const path = window.location.pathname;
    const id = path.substring(path.lastIndexOf('/') + 1);
    const segment = path.split('/');

    delButton.addEventListener('click', () => {
        fetch(`/api/lists/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf').innerHTML,
            }
        });
        window.location.href = `/users/${segment[2]}/lists`
    });

    const editButton = document.getElementById('edit');
    editButton.addEventListener('click', () => {
        const head = document.getElementById('head');
        const editWindow = document.getElementById('edit_window');

        const title = document.getElementById('title');
        const body = document.getElementById('desc');

        let titleInput = document.getElementById('title_input');
        let bodyInput = document.getElementById('desc_input');

        if (editWindow.style.display === 'block') {
            if (editButton.innerHTML === 'Save') {
                fetch(`/api/lists/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.getElementById('csrf').innerHTML,
                    },
                    body: JSON.stringify({
                        title: `${titleInput.value}`,
                        desc: `${bodyInput.value}`,
                        action: 'edit'
                    })
                });
            }
            title.innerHTML = `${titleInput.value}`;
            body.innerHTML = `${bodyInput.value}`;

            head.style.display = 'block';
            editWindow.style.display = 'none';
            editButton.innerHTML = 'Edit';
            
            editButton.classList.add('btn-outline-primary');
            editButton.classList.remove('btn-primary');

        } else {
            head.style.display = 'none';
            editWindow.style.display = 'block';
            editButton.innerHTML = 'Save';
            editButton.classList.add('btn-primary');
            editButton.classList.remove('btn-outline-primary');

            titleInput.value = `${title.innerHTML}`;
            bodyInput.value = `${body.innerHTML}`;
        }
    });
});

