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
    // IMPORTANTE: Evite responder mensagens que o próprio bot enviou para não entrar em loop
    if (message.fromMe) return;

    const messageData = {
        sender: message.from,
        body: message.body
    };

    try {
        const response = await fetch('http://localhost:8080/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(messageData)
        });

        if (response.ok) {
            // O Spring Boot deve retornar o texto da resposta no corpo (body)
            const response = await response.text(); 
            
            if (response && response.trim() !== "") {
                // Envia a resposta da IA de volta para o número que enviou a mensagem
                await client.sendMessage(message.from, response);
                console.log('Resposta da enviada com sucesso');
            }
        } else {
            console.error('Spring Boot service error: ', response.statusText);
        }
    } catch (error) {
        console.error('Fatal error trying to connect to Spring Boot service:', error.message);
    }
});


