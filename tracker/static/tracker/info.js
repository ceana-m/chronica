document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const id = path.substring(path.lastIndexOf('/') + 1);
    console.log(id);

    let mediaType;
    if (path.includes('movies')) {
        mediaType = 'movie';
    }

    
});
