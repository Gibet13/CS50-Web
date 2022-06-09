document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('form').onsubmit = send_mail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach(email => {
        mail_info = document.createElement('div');
        mail_info.classList.add("mail_info");

        if (email.read == true)
          {mail_info.style.backgroundColor = "rgb(235,235,235)"}

        sender = document.createElement('div');
        sender.classList.add("recipient");
        if (mailbox == 'sent')
          {sender.innerHTML = `${email.recipients}`;}
        else 
          {sender.innerHTML = `${email.sender}`;}

        subject = document.createElement('div');
        subject.classList.add("subject");
        subject.innerHTML = `${email.subject}`;
        subject.addEventListener('click', function() {
          show_mail(email.id)
        });
        archive_toggle = document.createElement('div');
        button = document.createElement('button');
        button.classList.add("btn", "btn-outline-primary");
        button.innerHTML = 'archive';
        button.addEventListener('click', function() {
          archive(email.id)
        });
        archive_toggle.append(button);

        date =  document.createElement('div');
        date.classList.add("timestamp");
        date.innerHTML = `${email.timestamp}`;

        mail_info.append(sender, subject, date, archive_toggle)

        document.querySelector('#emails-view').append(mail_info);
      });
    });

}

function send_mail() {

  
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  localStorage.clear();
  load_mailbox('sent');
  return false;
}

function show_mail(id) {

  // Show mail view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(emails => {
      // Print email
      console.log(emails);

    // ... do something else with email ...
    document.querySelector('#mail-view').innerHTML = "";
    mail_content = document.createElement('div');
    mail_content.classList.add("mail_content");

    sender = document.createElement('div');
    sender.innerHTML = `<b>From</b>: ${emails.sender}`;

    recipients = document.createElement('div');
    recipients.innerHTML = `<b>To</b>: ${emails.recipients}`;

    subject = document.createElement('div');
    subject.innerHTML = `<b>Subject</b>: ${emails.subject}`;

    timestamp = document.createElement('div');
    timestamp.innerHTML = `<b>Date</b>: ${emails.timestamp}`;

    body = document.createElement('div');
    body.classList.add("mail_body");
    body.innerHTML = `${emails.body}`;

    reply_button = document.createElement('button');
    reply_button.classList.add("btn", "btn-outline-primary");
    reply_button.addEventListener('click', function() {
        reply_mail(emails.id)
    });
    reply_button.innerHTML = 'Reply';

    mail_content.append(sender, recipients, subject, timestamp, body, reply_button);

    document.querySelector('#mail-view').append(mail_content);
  });
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(emails => {

    if (emails.archived == false) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
    }

    else {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
    }
  });
  localStorage.clear();
  load_mailbox('archive');
}

function reply_mail(id) {
  compose_email();
  
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // ... do something else with email ...
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  });
}