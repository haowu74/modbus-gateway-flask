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
    if (isNaN(parseInt(text.value)) || text.value <= 0) {
        text.value = text.oldValue;
    }
}

function registerChanged(text) {
    if (isNaN(parseInt(text.value)) || text.value < 0) {
        text.value = text.oldValue;
    }
}

function delayChanged(text) {
    if (isNaN(parseInt(text.value)) || text.value <= 0) {
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

async function config() {
	await fetch("/config")
	.then((res) => {
		location.href = "/config";
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

async function addNewUser() {
    let username = document.getElementById("new-user-name").value;
    let password = document.getElementById("new-user-password").value;
    let repeat = document.getElementById("new-user-password-repeat").value;
    if (password === repeat) {
        await fetch("/addnewuser", {
            method: "POST",
            body: JSON.stringify({
                username: username,
                password: password
            })
        }).then((res) => {
            return res.json();
        }).then((data) => {
            if (data.success) {
                location.reload();
            } else {
                document.getElementById("create-new-user-failed").showModal();
            }
        });
    } else {
        document.getElementById("change-password-repeat-failed").showModal();
    }
    
};

async function changePassword() {
    let username = document.getElementById("user-to-change-password").innerHTML;
    let password = document.getElementById("new-password").value;
    let repeat = document.getElementById("new-password-repeat").value;
    if (password === repeat) {
        await fetch("/changepassword", {
            method: "POST",
            body: JSON.stringify({
                username: username,
                password: password
            })
        }).then((res) => {
            return res.json();
        }).then((data) => {
            if (data.success) {
                document.getElementById("change-password-success").showModal();
            } else {
                document.getElementById("change-password-failed").showModal();
            }
        });
    } else {
        document.getElementById("change-password-repeat-failed").showModal();
    }
}

async function deleteUser() {
    let username = document.getElementById("user-to-delete").innerHTML;
    await fetch("/deleteuser", {
        method: "POST",
        body: JSON.stringify({
            username: username
        })
    }).then((res) => {
        return res.json();
    }).then((data) => {
        if (data.success) {
            location.reload();
        }
    });
}

function toggkeSelectAll() {
    let checkboxes = document.getElementsByClassName('config-table')[0].querySelectorAll('.config-selector');
    if (document.getElementById('select_all').checked) {
        for (var i in checkboxes) {
            checkboxes[i].checked = true;
        }
    } else {
        for (var i in checkboxes) {
            checkboxes[i].checked = false;
        }
    }
}

function unlock() {
    document.getElementById('license-dlg').showModal();
}

async function inputLicenseCode() {

}
