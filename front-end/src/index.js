const movie_list = document.querySelector('ul.movies');
const movie_items = movie_list.getElementsByTagName('li');

async function uploadFile(file_to_send, movie_name, user_name) {
    let formData = new FormData();
    formData.append("file", file_to_send);
    await fetch('http://elmo4679.pythonanywhere.com/add_comment?' + new URLSearchParams({
        'movie_name': movie_name,
        'user_name': user_name,
    }), {
        method: "POST",
        body: formData
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        });
    alert('The file has been uploaded successfully.');
}

async function getComments(movie_name, language) {
    return await fetch('http://elmo4679.pythonanywhere.com/get_comments?' + new URLSearchParams({
        'movie_name': movie_name,
        'language': language
    }), {
        method: "GET",
    })
}

function handleShowComments(data) {
    let result = "";
    let comments = Object.keys(data['comments'])
    comments.forEach((key, index) => {
        const id = key;
        const user_name = data['comments'][key]['user_name'];
        const movie_name = data['comments'][key]['movie_name'];
        const comment = data['comments'][key]['comment'];
        result += `<li>
                    <div class="comment-user-name">${user_name}</div>
                    <div class="comment-movie-name">(${movie_name}):</div>
                    <div class="comment-comment">${comment}</div>
                </li>`;
    });
    return result;
}


function addListeners(movie_counts, add_comment_button, view_comments_button, english_button, russian_button, german_button, exit_button) {
    for (let i = 0; i < movie_counts; i++) {
        const button = add_comment_button[i];
        button.addEventListener('click', function () {
            const movie_item = button.parentNode;
            const title = movie_item.getElementsByTagName('h2')[0].innerText;
            const director = movie_item.getElementsByTagName('h3')[0].innerText;
            const add_file = movie_item.querySelector('input.add-file');
            const username = movie_item.querySelector('input.username');
            add_file.style.display = 'block';
            username.style.display = 'block';

            add_file.addEventListener('change', function () {
                let file_to_send = add_file.files[0];
                uploadFile(file_to_send, title, username.value);
                add_file.type = 'text';
                add_file.type = 'file';
                add_file.style.display = 'None';
                username.style.display = 'None';
            });
            console.log(`Adding comment for ${title} by ${director}`);
        });
    }

    for (let i = 0; i < movie_counts; i++) {
        const button = view_comments_button[i];
        button.addEventListener('click', function () {
            const movie_item = button.parentNode;
            const title = movie_item.getElementsByTagName('h2')[0].innerText;
            const director = movie_item.getElementsByTagName('h3')[0].innerText;
            const languages = movie_item.querySelector('div');
            languages.style.display = 'block';
            console.log(`Viewing comments for ${title} by ${director}`);
        });
    }

    for (let i = 0; i < movie_counts; i++) {
        const button = view_comments_button[i];
        english_button[i].addEventListener('click', function () {
            const movie_item = button.parentNode;
            const title = movie_item.getElementsByTagName('h2')[0].innerText;
            const director = movie_item.getElementsByTagName('h3')[0].innerText;
            console.log(`Viewing comments for ${title} by ${director} in English`);
            getComments(title, 'en').then(response => response.json())
                .then(data => {
                    movie_item.style.display = 'none';
                    movie_list.innerHTML += handleShowComments(data) + `<button class="exit-button" onclick="setMovies()" = 'flex'">Exit</button>`;
                });
        });

        russian_button[i].addEventListener('click', function () {
            const movie_item = button.parentNode;
            const title = movie_item.getElementsByTagName('h2')[0].innerText;
            const director = movie_item.getElementsByTagName('h3')[0].innerText;
            console.log(`Viewing comments for ${title} by ${director} in Russian`);
            getComments(title, 'ru').then(response => response.json())
                .then(data => {
                    movie_item.style.display = 'none';
                    movie_list.innerHTML += handleShowComments(data) + `<button class="exit-button" onclick="setMovies()" = 'flex'">Exit</button>`;

                });
        });

        german_button[i].addEventListener('click', function () {
            const movie_item = button.parentNode;
            const title = movie_item.getElementsByTagName('h2')[0].innerText;
            const director = movie_item.getElementsByTagName('h3')[0].innerText;
            console.log(`Viewing comments for ${title} by ${director} in German`);
            getComments(title, 'de').then(response => response.json())
                .then(data => {
                    movie_item.style.display = 'none';
                    movie_list.innerHTML += handleShowComments(data) + `<button class="exit-button" onclick="setMovies()" = 'flex'">Exit</button>`;
                });
        });
    }

}

function setMovies() {
    fetch('http://elmo4679.pythonanywhere.com/get_movies')
        .then(response => response.json())
        .then(data => {
            let keys = Object.keys(data['movies']);
            movie_list.innerHTML = '';
            keys.forEach((key, index) => {
                const movieName = key;
                const movieDirector = data['movies'][key]['director'];
                const moviePoster = data['movies'][key]['poster'];
                movie_list.innerHTML += `<li class="movie-item">
                                            <input type="text" style="width: 200px; height: 200px;"/>
                                            <img src=${moviePoster} alt="">
                                            <h2>${movieName}</h2>
                                            <h3>${movieDirector}</h3>
                                            <button class="add-comment">Add comment</button>
                                            <input class="add-file" type="file" name="file">
                                            <input class="username" placeholder="enter your name:" type="text" name="username">
                                            <button class="view-comments">View comments</button>
                                            <div class="languages">
                                                <button class="english">English</button>
                                                <button class="russian">Russian</button>
                                                <button class="german">German</button>
                                            </div>
                                        </li>`;
            });
            const add_comment_button = document.querySelectorAll('button.add-comment');
            const view_comments_button = document.querySelectorAll('button.view-comments');
            const english_button = document.querySelectorAll('button.english');
            const russian_button = document.querySelectorAll('button.russian');
            const german_button = document.querySelectorAll('button.german');
            const movie_counts = movie_items.length;
            const exit_button = document.querySelector('.exit');

            addListeners(movie_counts, add_comment_button, view_comments_button, english_button, russian_button, german_button, exit_button);
        });
}

setMovies();