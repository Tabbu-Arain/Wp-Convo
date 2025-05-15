import { makeWASocket, useMultiFileAuthState } from '@whiskeysockets/baileys';
import qrcode from 'qrcode';

const __dirname = new URL('.', import.meta.url).pathname;

// Store QR in a file for Flask to read
async function saveQR(qrData) {
  const qrImage = await qrcode.toDataURL(qrData);
  await fs.writeFile(path.join(__dirname, 'qr.png'), qrImage.split(',')[1], 'base64');
}

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState('./auth_info');
  const sock = makeWASocket({ auth: state });

  sock.ev.on('connection.update', async (update) => {
    if (update.qr) {
      await saveQR(update.qr); // Save QR as image file
    }
    if (update.connection === 'open') {
      console.log("WhatsApp connected!");
    }
  });

  sock.ev.on('creds.update', saveCreds);
}

startBot().catch(console.error);
