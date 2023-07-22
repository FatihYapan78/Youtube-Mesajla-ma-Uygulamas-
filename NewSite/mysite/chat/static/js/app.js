const roomName = JSON.parse(document.getElementById('room-name').textContent);
const conservation = document.getElementById('conversation');
        // Connection / Bağlantı 
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );
        // WEbSoketten veri geldiğinde çalışır.
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            var message = `<div class="row message-body">
            <div class="col-sm-12 message-main-sender">
            <div class="sender">
                <div class="message-text">
                ${data.message}
                </div>
                <span class="message-time pull-right">
                Sun
                </span>
            </div>
            </div>
        </div>`
        conservation.innerHTML += message;
        };
        // WEbSoketten bağlantısı kapandığında 
        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
        // Sayfa açıldığında inputa odaklar
        document.querySelector('#comment').focus();
        // Enter tuşuna basıldığında mesajı göndermek için

        document.querySelector('#comment').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#send').click();
            }
        };
        // Mesajın json'a çevirilirip gönderilmesi işin yapar.
        document.querySelector('#send').onclick = function(e) {
            const messageInputDom = document.querySelector('#comment');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };