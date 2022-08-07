function save(button) {
    var units = [];
    for (var i = 1; i < 201; i++) {
        var row = button.parentElement.parentElement.parentElement.querySelector(`#select_${i}`).parentElement.parentElement;
        var selected = row.querySelector("input[type='checkbox']").checked;
        var id = row.querySelector(".unit-number").value;
        var address = row.querySelector(".modbus-address").value;
        var register = row.querySelector(".holding-register").value;
        var delay = row.querySelector(".delay-time").value;
        var unit = {
            selected: selected,
            id: id,
            address: address,
            register: register,
            delay: delay
        }
        units.push(unit);
    }
	fetch("/save", {
		method:"POST",
		headers: {
			"Content-type": "application/json",
		},
		body: JSON.stringify(units),
	})
	.then((res)=> {
	    return res.json();
	}).then(data => {
		if (data.success) {
			document.getElementById("save-success").showModal();
		} else {
			document.getElementById("save-fail").showModal();
		}
	});
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

function delayChanged(text) {
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

async function logout() {
    await fetch("/logout", {method:"POST"})
	.then((res)=> {
	    location.href = "/login";
	});
}

async function admin() {
	await fetch("/admin")
	.then((res) => {
		location.href = "/admin";
	});
}

async function download() {
    await fetch("/download", {method:"POST"})
	.then((res)=> {
	    return res.blob();
	}).then(blob => {
	    var a = document.createElement("a");
	    a.href = URL.createObjectURL(blob);
	    a.setAttribute("download", "config.json");
	    a.click();
	    a.remove();
	});
}


async function upload() {
    let formData = new FormData();
    formData.append("file", fileupload.files[0]);
    await fetch("/upload", {
	method:"POST",
        body: formData
    }).then((res) => {
    	return res.json();
    }).then((data) => {
    	if (data.success) {
			document.getElementById("upload-success").showModal();
		} else {
			document.getElementById("upload-fail").showModal();
		}
    });
}

