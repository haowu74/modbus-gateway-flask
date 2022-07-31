function save(button) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/save", true);
    xhttp.setRequestHeader("Content-type", "application/json; charset=UTF-8");
    var units = [];
    for (var i = 1; i < 201; i++) {
        var row = button.parentElement.parentElement.parentElement.querySelector(`#select_${i}`).parentElement.parentElement;
        var selected = row.querySelector("input[type='checkbox']").checked;
        var id = row.querySelector(".unit-number").value;
        var address = row.querySelector(".modbus-address").value;
        var register = row.querySelector(".holding-register").value;
        var unit = {
            selected: selected,
            id: id,
            address: address,
            register: register,
        }
        units.push(unit);
    }
    xhttp.send(JSON.stringify(units));
}

function addressChanged(text) {
    if (isNaN(parseFloat(text.value)) ) {
        text.value = text.oldValue;
    }
}

function registerChanged(text) {
    if (isNaN(parseFloat(text.value)) ) {
        text.value = text.oldValue;
    }
}

function unitSelected(checkbox) {
    var id = parseInt(checkbox.id.split('_')[1]);
    var checked = checkbox.checked;
    if (!checked) {
        checkbox.parentElement.parentElement.querySelector(".modbus-address").readOnly = false;
        checkbox.parentElement.parentElement.querySelector(".holding-register").readOnly = false;
    } else {
        checkbox.parentElement.parentElement.querySelector(".modbus-address").readOnly = true;
        checkbox.parentElement.parentElement.querySelector(".holding-register").readOnly = true;
    }
}

