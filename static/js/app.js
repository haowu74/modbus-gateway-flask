function save() {
    console.log("Saved");
    const xhttp = new XMLHttpRequest();
    
    xhttp.open("POST", "/save", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("name=hello");
}