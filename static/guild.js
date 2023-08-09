function addRemoveRestoreButtons() {
    var dictItems = document.querySelectorAll('.dict-item');

    dictItems.forEach(function (item) {
        var input = item.querySelector('.form-control');
        var removeButton = item.querySelector('.remove-button');
        var restoreButton = item.querySelector('.restore-button');

        // Add event listeners to remove and restore buttons
        removeButton.addEventListener('click', function () {
            item.classList.toggle('marked-for-deletion');
            toggleButtons(item);
        });

        restoreButton.addEventListener('click', function () {
            item.classList.toggle('marked-for-deletion');
            toggleButtons(item);
        });

        // Toggle buttons based on item state
        toggleButtons(item);

        // Add event listener to input field for changes
        input.addEventListener('input', function () {
            item.classList.remove('marked-for-deletion');
            toggleButtons(item);
        });
    });
}

function toggleButtons(item) {
    var input = item.querySelector('.form-control');
    var removeButton = item.querySelector('.remove-button');
    var restoreButton = item.querySelector('.restore-button');

    if (item.classList.contains('marked-for-deletion')) {
        input.style.backgroundColor = '#ffcccc'; // Change background color
        if (removeButton) {
            removeButton.style.display = 'none';
        }
        if (restoreButton) {
            restoreButton.style.display = 'block';
        }
    } else {
        input.style.backgroundColor = ''; // Reset background color
        if (removeButton) {
            removeButton.style.display = 'block';
        }
        if (restoreButton) {
            restoreButton.style.display = 'none';
        }
    }
}


function toggleAllButtons() {
    var dictItems = document.querySelectorAll('.dict-item');
    dictItems.forEach(function (item) {
        toggleButtons(item);
    });
}

function saveSettings() {
    var changedSettings = {};

    // Iterate through input fields and check for changes
    var inputFields = document.querySelectorAll('input[type="text"]');

    inputFields.forEach(function (input) {
        var idParts = input.id.split('|||');
        var valueType = idParts[0];
        var settingName = idParts[1];
        var valueName = idParts[2];
        var newValue = input.value;
        var originalValue = input.getAttribute('data-original-value');

        if (valueType === 'list') {
            if (newValue !== originalValue) {
                // Store the change in the dictionary
                if (newValue == "") {
                    return;
                }
                changedSettings[settingName] = newValue;
            }
        } else if (valueType === 'nonedit') {
            // Handle non-editable values
            return; // Skip processing for non-editable values
        } else {
            if (newValue !== originalValue) {
                // Store the change in the dictionary
                var name = valueType.split(":")[0];
                if (name === "bot_prefix" || name == "default_cash") {
                    return;
                }
                changedSettings[name] = newValue;
            }
        }
    });

    // Check if any changes were detected
    if (Object.keys(changedSettings).length === 0) {
        alert('No changes to save.');
        return;
    }

    // Send POST request for changed settings
    fetch('http://localhost:2710/api/settings/update/87350819', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(changedSettings)
    })
    .then(response => {
        if (response.status === 200) {
            alert('Settings saved successfully');
            // ... (rest of your success handling code)
        } else {
            alert('Error: Failed to save settings');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



// Call the addRemoveRestoreButtons function to enable remove/restore button functionality
document.addEventListener('DOMContentLoaded', function () {
    addRemoveRestoreButtons();
});


