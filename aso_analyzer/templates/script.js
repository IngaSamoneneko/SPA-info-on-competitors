const apps = [
  {
    "bundle_id": "com.whatsapp",
    "title": "WhatsApp Messenger",
    "developer_name": "WhatsApp LLC",
    "google_play_url": "https://play.google.com/store/apps/details?id=com.whatsapp",
    "icon": "https://play-lh.googleusercontent.com/bYtqbOcTYOlgc6gqZ2rwb8lptHuwlNE75zYJu6Bn076-hTmvd96HH-6v7S0YUAAJXoJN"
  },
  {
    "bundle_id": "com.whatsapp.w4b",
    "title": "WhatsApp Business",
    "developer_name": "WhatsApp LLC",
    "google_play_url": "https://play.google.com/store/apps/details?id=com.whatsapp.w4b",
    "icon": "https://play-lh.googleusercontent.com/K6L_Ixmw0J9oTktAoHyEHvzQIfxEF1CIQ5aE0WHhdUeOgfAmn7KLhe47Q5XxZaXQ0g"
  },
  // Add other apps here...
];

const container = document.getElementById('app-list');

apps.forEach(app => {
  const card = document.createElement('div');
  card.className = 'app-card';

  card.innerHTML = `
    <img src="${app.icon}" alt="${app.title} icon" />
    <div>
      <h3>${app.title}</h3>
      <p><strong>Developer:</strong> ${app.developer_name}</p>
      <a href="${app.google_play_url}" target="_blank">Open in Play Store</a>
    </div>
  `;

  container.appendChild(card);
});
