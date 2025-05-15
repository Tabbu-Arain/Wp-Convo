const { exec } = require('child_process');
const fs = require('fs');

// Modified version of your original script (save as index.js)
async function startWhatsApp() {
  const { makeWASocket, useMultiFileAuthState } = await import('@whiskeysockets/baileys');
  
  const { state, saveCreds } = await useMultiFileAuthState('./auth_info');
  const sock = makeWASocket({ auth: state });

  sock.ev.on('connection.update', (update) => {
    if (update.qr) {
      console.log('QR CODE:', update.qr);  // Flask will read this
    }
    if (update.connection === 'open') {
      console.log('WhatsApp connected!');
    }
  });

  sock.ev.on('creds.update', saveCreds);
}

// Start the script
startWhatsApp().catch(console.error);
