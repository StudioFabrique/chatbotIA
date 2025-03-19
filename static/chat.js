function envoyerMessage(){
    const message = document.getElementById("message").value;
    const zoneMessages = document.getElementById("zoneMessages");

    //push le message de l'utilisateur
    const nouveau_msg = document.createElement("div");
    nouveau_msg.textContent = message;
    nouveau_msg.className = "user_message";
    zoneMessages.append(nouveau_msg);
    document.getElementById("message").value = ""

    //envoyer le message au backend
    var messageJson = {message : message};
    fetch('/get', {
        method : "POST",
        headers : { "content-type" : "application/json"},
        body : JSON.stringify(messageJson)
    })
    .then(function(response) {
        return response.text();
    }).then(function(data){
        //push la reponse
        const reponse = document.createElement("div");
        reponse.textContent = data;
        reponse.className = "answer";
        zoneMessages.append(reponse);
    });

    

}