document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#all').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));

    document.querySelector("#post-form").onsubmit = create_post;
    

    //default
    load_posts('all');
})

function create_post() {

    const title = document.querySelector("#post-title").value;
    const body = document.querySelector("#post-body").value;

    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            title: title,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
}

function load_posts(postbox) {

    document.querySelector('#create-post-view').style.display = 'block';
    document.querySelector('#edit-post-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#post-view').style.display = 'none';
    

    document.querySelector('#posts-view').innerHTML = `<h3>${postbox.charAt(0).toUpperCase() + postbox.slice(1)}</h3>`;

    fetch(`/posts/${postbox}`)
    .then(response => response.json())
    .then(posts => {
      // Print posts
      console.log(posts);

      posts.forEach(post => {
        postbox = document.createElement('div');
        postbox.classList.add('post_box');

        author = document.createElement('div');
        author.addEventListener('click', () => load_profile(post.author_id))
        author.classList.add('post_author');
        author.innerHTML = `<b>${post.author}</b>`;

        title = document.createElement('div');
        title.classList.add('post_title');
        title.innerHTML = `${post.title}`;
        title.addEventListener('click', () => show_post(post.id))

        body = document.createElement('div');
        body.classList.add('post_body');
        body.innerHTML = `${post.body}`;

        date = document.createElement('div');
        date.classList.add('post_date');
        date.innerHTML = `${post.date}`;

        like = document.createElement('button');
        like.addEventListener('click', () => like_post(post.id));
        like.innerHTML = 'like'

        postbox.append(author, title, body, date, like);

        document.querySelector('#posts-view').append(postbox);
        });
    });
}

function load_profile(user_id) {
    
    document.querySelector('#create-post-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'block';
    document.querySelector('#post-view').style.display = 'none';
    
    fetch(`/profile/${user_id}`)
    .then(response => response.json())
    .then(profile => {
        console.log(profile);

        document.querySelector('#profile-view').innerHTML = `<h3>${profile[0]['name'].charAt(0).toUpperCase() + profile[0]['name'].slice(1)}'s Profile</h3>`;
        document.querySelector('#posts-view').innerHTML = `<h3>${profile[0]['name'].charAt(0).toUpperCase() + profile[0]['name'].slice(1)}'s Posts</h3>`;

        profilebox = document.createElement('div');
        profilebox.classList.add('profile_box');

        username = document.createElement('div');
        username.innerHTML = `<b>${profile[0]['name']}</b>`;
        
        followers = document.createElement('div');
        followers.innerHTML = `followers: ${profile[0]['followers']}`;

        following = document.createElement('div');
        following.innerHTML = `following: ${profile[0]['following']}`;

        follow_button = document.createElement('button');
        follow_button.addEventListener('click', () => follow_user(profile[0]['id']));
        follow_button.innerHTML = 'Follow'

        profilebox.append(username, following, followers, follow_button);

        document.querySelector('#profile-view').append(profilebox);

        profile[1].forEach(post => {

            postbox = document.createElement('div');
            postbox.classList.add('post_box');

            author = document.createElement('div');
            author.addEventListener('click', () => load_profile(post.author_id))
            author.innerHTML = `<b>${post.author}</b>`;

            title = document.createElement('div');
            title.innerHTML = `${post.title}`;

            body = document.createElement('div');
            title.addEventListener('click', () => show_post(post.id));
            body.innerHTML = `${post.body}`;

            date = document.createElement('div');
            date.innerHTML = `${post.date}`;

            like = document.createElement('button');
            like.addEventListener('click', () => like_post(post.id));
            like.innerHTML = 'like'

            postbox.append(author, title, body, date, like);

            document.querySelector('#posts-view').append(postbox);
        })
    });
}

function show_post(post_id){

    document.querySelector('#post-view').style.display = 'block';
    document.querySelector('#create-post-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';
    
    document.querySelector('#comment-form').addEventListener('submit', () => post_comment(post_id));
    document.querySelector('#edit-form').addEventListener('submit', () => edit_post(post_id));

    document.querySelector('#post').innerHTML = "";
    document.querySelector('#comments').innerHTML = "<h5>Comments</h5>";

    fetch(`/posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);
        
        author = document.createElement('div');
        author.addEventListener('click', () => load_profile(post.author_id))
        author.innerHTML = `<b>${post.author}</b>`;

        title = document.createElement('div');
        title.innerHTML = `${post.title}`;

        body = document.createElement('div');
        body.innerHTML = `${post.body}`;

        date = document.createElement('div');
        date.innerHTML = `${post.date}`;

        like = document.createElement('button');
        like.addEventListener('click', () => like_post(post.id));
        like.innerHTML = `${post.like_count} like`

        edit = document.createElement('button');
        edit.innerHTML = 'edit'
        edit.addEventListener('click', () => {

            document.querySelector('#post-view').style.display = 'none';
            document.querySelector('#edit-post-view').style.display = 'block';

            document.querySelector('#edit-title').value = `${post.title}`;
            document.querySelector('#edit-body').innerHTML = `${post.body}`;
        });

        document.querySelector('#post').append(author, title, body, date, like, edit);
    })

    fetch(`/posts/${post_id}/comments`)
    .then(response => response.json())
    .then(comments => {
        console.log(comments);

        comments.forEach(comment => {
            commentbox = document.createElement('div');
            commentbox.classList.add('comment_box');

            author = document.createElement('div');
            author.addEventListener('click', () => load_profile(comment.author_id))
            author.innerHTML = `<b>${comment.author}</b>`;

            date = document.createElement('div');
            date.innerHTML = `${comment.date}`;

            body = document.createElement('div');
            body.classList.add('comment_body');
            body.innerHTML = `${comment.body}`;

            info = document.createElement('div');
            info.classList.add('comment_info');
            info.append(author, date);

            commentbox.append(info, body);
            document.querySelector('#comments').append(commentbox);
        });        
    });
}

function edit_post(post_id) {

    title = document.querySelector("#edit-title").value;
    body = document.querySelector("#edit-body").value;

    fetch(`posts/edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            title: title,
            body: body,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });

      document.querySelector('#edit-post-view').style.display = 'none';

      show_post(post_id);
      return false;
}

function post_comment(post_id) {

    const body = document.querySelector("#comment-body").value;

    fetch(`comment/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            body: body,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });

      show_post(post_id);
}

function like_post(post_id) {
    fetch(`like/${post_id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

function follow_user(user_id) {
    fetch(`follow/${user_id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}