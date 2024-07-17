//----------------------------------enviar al correo electronico un mensaje, utilicé la aplicación EmailJS.com----------------------------------
const btn = document.getElementById('button');

document.getElementById('form')
 .addEventListener('submit', function(event) {
   event.preventDefault();

    const btn = document.getElementById('button');
    const terms = document.getElementById('terms');

    if (!terms.checked) {
        alert('Por favor, Acepta los términos y condiciones de SuperDuper.');
        return;
    }

   btn.value = 'Enviando...';

   const serviceID = 'default_service';
   const templateID = 'template_o6xiukq';

   emailjs.sendForm(serviceID, templateID, this)
    .then(() => {
      btn.value = 'Enviar Suscripción';
      alert('¡Suscripción enviada correctamente!');
    }, (err) => {
      btn.value = 'Enviar Suscripción';
      alert(JSON.stringify(err));
    });
});