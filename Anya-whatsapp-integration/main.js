const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client();

client.once('ready', () => {
    console.log('Client is ready!');
});

client.on('qr', (qr) => {
    qrcode.generate(qr, {small: true});
});

client.initialize();

client.on('message_create', async (message) => {

    if (message.fromMe) {
        return;
    }

    const messageData = {
        contact: message.from,
        account: client.info.wid.user,
        body: message.body,

    };

    try {
        const response = await fetch('http://localhost:8000/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(messageData)
        });

        if (response.ok) {
            // O Spring Boot deve retornar o texto da resposta no corpo (body)
            const responseData = await response.json();
            
            if (responseData && responseData.body && responseData.body.trim() !== "") {
                // Envia a resposta da IA de volta para o número que enviou a mensagem
                await client.sendMessage(message.from, responseData.body);
                console.log('Resposta da enviada com sucesso');
            }
        } else {
            console.error('Spring Boot service error: ', response.statusText);
        }
    } catch (error) {
        console.error('Fatal error trying to connect to Spring Boot service:', error.message);
    }
});


