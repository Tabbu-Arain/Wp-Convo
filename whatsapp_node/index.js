import { makeWASocket, useMultiFileAuthState } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState(
    path.join(__dirname, 'auth_info')
  );

  const sock = makeWASocket({ auth: state });

  sock.ev.on('connection.update', (update) => {
    if (update.qr) {
      qrcode.generate(update.qr, { small: true });
      console.log("[FLASK] QR code generated");
    }
    if (update.connection === 'open') {
      console.log("[FLASK] WhatsApp connected");
    }
  });

  sock.ev.on('creds.update', saveCreds);
}

startBot().catch(console.error);
