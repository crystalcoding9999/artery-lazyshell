/*
const deleteColor = '#ffcccc'

function addRemoveRestoreButtons() {
    var dictItems = document.querySelectorAll('.dict-item');

    dictItems.forEach(function (item) {
        let id = item.id;
        if (id.startsWith("list")) {
            let listInput = item.querySelector('.form-control');
            let listRemoveButton = item.querySelector('.remove-button');
            let listRestoreButton = item.querySelector('.restore-button');

            if (listInput && listRemoveButton && listRestoreButton) {
                // Add event listeners to remove and restore buttons
                listRemoveButton.addEventListener('click', function () {
                    item.classList.toggle('marked-for-deletion');
                    toggleButtons(item);
                });

                listRestoreButton.addEventListener('click', function () {
                    item.classList.toggle('marked-for-deletion');
                    toggleButtons(item);
                });

                // Toggle buttons based on item state
                toggleButtons(item);

                // Add event listener to input field for changes
                listInput.addEventListener('input', function () {
                    item.classList.remove('marked-for-deletion');
                    toggleButtons(item);
                });
            }
        } else if (id.startsWith("dict")) {
            let dictNameInput = item.querySelector('.dict-name');
            let dictValueInput = item.querySelector('.dict-value');
            let dictRemoveButton = item.querySelector('.remove-button');
            let dictRestoreButton = item.querySelector('.restore-button');

            if (dictNameInput && dictRemoveButton && dictRestoreButton) {
                // Add event listeners to remove and restore buttons
                dictRemoveButton.addEventListener('click', function () {
                    item.classList.toggle('marked-for-deletion');
                    toggleDictButtons(item);
                });

                dictRestoreButton.addEventListener('click', function () {
                    item.classList.toggle('marked-for-deletion');
                    toggleDictButtons(item);
                });

                // Toggle buttons based on item state
                toggleDictButtons(item);

                // Add event listener to input field for changes
                dictNameInput.addEventListener('input', function () {
                    item.classList.remove('marked-for-deletion');
                    toggleDictButtons(item);
                });

                // Add event listener to input field for changes
                dictValueInput.addEventListener('input', function () {
                    item.classList.remove('marked-for-deletion');
                    toggleDictButtons(item);
                });
            }
        }
    });
}

function toggleButtons(item) {
    let input = item.querySelector('.form-control');
    let removeButton = item.querySelector('.remove-button');
    let restoreButton = item.querySelector('.restore-button');

    if (item.classList.contains('marked-for-deletion')) {
        input.style.backgroundColor = deleteColor; // Change background color
        removeButton.style.display = 'none';
        restoreButton.style.display = 'block';
    } else {
        input.style.backgroundColor = ''; // Reset background color
        removeButton.style.display = 'block';
        restoreButton.style.display = 'none';
    }
}

function toggleDictButtons(item) {
    let nameInput = item.querySelector('.dict-name');
    let valueInput = item.querySelector('.dict-value')
    let removeButton = item.querySelector('.remove-button');
    let restoreButton = item.querySelector('.restore-button');

    if (item.classList.contains('marked-for-deletion')) {
        nameInput.style.backgroundColor = deleteColor; // Change background color
        valueInput.style.backgroundColor = deleteColor; // Change background color
        removeButton.style.display = 'none';
        restoreButton.style.display = 'block';
    } else {
        nameInput.style.backgroundColor = ''; // Reset background color
        valueInput.style.backgroundColor = ''; // Reset background color
        removeButton.style.display = 'block';
        restoreButton.style.display = 'none';
    }
}
*/

const apiURL = "http://localhost:2710"

function deleteValue(value) {
    let split = value.split('|')
    let name = ""
    if (split.length === 3) {
        name = split[2];
    } else if (split.length === 4) {
        name = split[3];
    }
    if (!confirm("are you sure you want to delete " + name.replace('_',' '))) {
        return;
    }

    let obj = document.getElementById(value);
    if (obj == null) {
        alert("something went wrong. please reload the page")
        return;
    }

    obj.remove();
    alert("deleted " + name.replace('_', ' '))
}

function addListItem(list) {
    let inputField = document.getElementById("list|" + list + ":new")
    if (inputField == null) {
        console.error("input field not found! (" + list + ")");
        return;
    }
    if (inputField.value === "") {
        alert("please insert a value");
        return;
    }

    let newID = "list|" + list + "|" + inputField.value;

    let template = "<li class=\"dict-item mb-3\" id=" + newID + ">\n" +
        "                                                <div class=\"d-flex align-items-center\">\n" +
        "                                                    <input type=\"text\" class=\"form-control\" id=" + newID + " value=" + inputField.value + ">\n" +
        "                                                    <button type=\"button\" class=\"btn btn-danger ms-2 remove-button\" onclick=\"deleteValue('" + newID + "')\">Remove</button>\n" +
        "                                                    <!-- <button type=\"button\" class=\"btn btn-success ms-2 restore-button\">Restore</button> -->\n" +
        "                                                </div>\n" +
        "                                            </li>"

    template = template.replace("{{ list }}", list);
    template = template.replace("{{ value }}", inputField.value);

    let holder_id = "list_{{ list }}_holder".replace("{{ list }}", list);
    document.getElementById(holder_id).insertAdjacentHTML("afterend",template);

    //addRemoveRestoreButtons()

    inputField.value = "";
}

function addDictItem(dict) {
    let nameInput = document.getElementById("dict|" + dict +"|key:new")
    let valueInput = document.getElementById("dict|" + dict +"|value:new")
    if (nameInput == null) {
        console.error("name input field not found! (" + dict + ")");
        return;
    }
    if (nameInput.value === "") {
        alert("please insert a name");
        return;
    }
    if (valueInput == null) {
        console.error("input field not found! (" + dict + ")");
        return;
    }
    if (valueInput.value === "") {
        alert("please insert a value");
        return;
    }

    let name = nameInput.value;
    let value = valueInput.value;

    let dictID = "dict|" + name;
    let newNameID = "dict|" + dict + "|key|" + name;
    let newValueID = "dict|" + dict + "|value|" + name + "|" + value;

    let template = "<li class=\"dict-item mb-3\" id=" + dictID + ">\n" +
        "               <div class=\"d-flex align-items-center\">" +
        "                   <input type=\"text\" class=\"form-control dict-name\" id=" + newNameID + " value=" + name +" disabled>\n" +
        "                   <input type=\"text\" class=\"form-control dict-value\" id=" + newValueID + " value=" + value + ">\n" +
        "                   <button type=\"button\" class=\"btn btn-danger ms-2 remove-button\" onclick=\"deleteValue('" + dictID + "')\">Remove</button>\n" +
        "                   <!-- <button type=\"button\" class=\"btn btn-success ms-2 restore-button\">Restore</button> -->\n" +
        "               </div>\n" +
        "           </li>";

    let holder_id = "dict_{{ name }}_holder".replace("{{ name }}", dict);
    document.getElementById(holder_id).insertAdjacentHTML("afterend", template);

    nameInput.value = "";
    valueInput.value = "";
}

function saveSettings() {
    let form = document.forms['settings-form'];
    if (form === null) {
        console.error("form not found!");
        alert("critical error reloading page");
        location.reload();
    }

    let formData = {};
    let changedListDict = {};
    let reload = false;

    for (let i = 0; i < form.length; i++) {
        let id = form[i].id;
        if (id.endsWith("new")) {
            continue;
        }
        if (id === "") {
            continue;
        }

        if (id.startsWith("list")) {
            let split = id.split("|");
            let listName = split[1];

            if (!(listName in changedListDict)) {
                changedListDict[listName] = [];
            }

            changedListDict[listName].unshift(form[i].value);
            continue;
        } else if (id.startsWith("dict")) {
            let split = id.split("|");
            if (split.length !== 5) {
                continue;
            }

            let dictName = split[1];
            let valueName = split[3];
            let valueValue = split[4];

            if (!(dictName in changedListDict)) {
                changedListDict[dictName] = {};
            }

            changedListDict[dictName][valueName] = valueValue;
            continue
        }

        formData[id] = form[i].value;
    }

    for (let key in changedListDict) {
        formData[key] = changedListDict[key];
    }

    console.log(formData);

    // Send POST request for changed settings
    fetch(apiURL + '/api/settings/update/87350819', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.status === 200) {
            alert('Settings saved successfully\nto prevent issues you will be redirected to another page');
        } else {
            alert('Error: Failed to save settings');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    location.replace(apiURL + "/dashboard")
}

function setupCollapsable() {
    let coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            let content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}


// Call the addRemoveRestoreButtons function to enable remove/restore button functionality
document.addEventListener('DOMContentLoaded', function () {
   setupCollapsable();
});




