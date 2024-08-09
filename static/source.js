function envoyerSource(){
    const source = document.getElementById("source").value;
    const zoneSource = document.getElementById("zoneSource");

    //push la source
    const nouvelle_source = document.createElement("div");
    nouvelle_source.textContent = source;
    nouvelle_source.className = "sourceUser";
    zoneSource.append(nouvelle_source);
    document.getElementById("source").value = "" 

    const zoneInfo = document.getElementById("info");
    zoneInfo.innerHTML = '';  //pour effacer l'info précédente
    const info = document.createElement("div");
    info.className = "info";
    info.textContent = "La source est en cours d'analyse";
    zoneInfo.append(info);
    //envoyer le message au backend
    var sourceJson = {source : source};
    fetch('/getSource', {
        method : "POST",
        headers : { "content-type" : "application/json"},
        body : JSON.stringify(sourceJson)
    })
    .then(function(response) {
        return response.text();
    }).then(function(data){
        //dire que la source est ajoutée
        info.textContent = data;
    });

}