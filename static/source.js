function envoyerSource(){
    const source = document.getElementById("source").value;
    const zoneSource = document.getElementById("zoneSource");

    //push la source
    const nouvelle_source = document.createElement("div");
    nouvelle_source.textContent = source;
    nouvelle_source.className = "sourceUser";
    zoneSource.append(nouvelle_source);
    document.getElementById("source").value = "" 

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
        const info = document.createElement("div");
        info.textContent = data;
        info.className = "info";
        const zoneInfo = document.getElementById("info");
        zoneInfo.innerHTML = '';  //pour effacer l'info précédente
        zoneInfo.append(info);
    });

}