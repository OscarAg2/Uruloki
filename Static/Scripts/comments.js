document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_comments')
        .then(response => response.json())
        .then(comments => {
            const carouselInner = document.querySelector('.carousel-inner');
            comments.forEach((comment, index) => {
                const activeClass = index === 0 ? 'active' : '';
                const commentHTML = `
                    <div class="carousel-item ${activeClass}">
                        <p class="bg-dark border rounded border-dark p-4">${comment.text}</p>
                        <div class="d-flex"><img class="rounded-circle flex-shrink-0 me-3 fit-cover" width="50" height="50" src="${comment.profile_photo_url}">
                            <div>
                                <p class="fw-bold text-primary mb-0">${comment.author_name}</p>
                                <p class="text-muted mb-0">${comment.author_type}</p>
                            </div>
                        </div>
                    </div>
                `;
                carouselInner.insertAdjacentHTML('beforeend', commentHTML);
            });
        })
        .catch(error => {
            console.error('Error fetching comments:', error);
        });
});
