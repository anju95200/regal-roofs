document.addEventListener('DOMContentLoaded', function () {
    // Smooth pagination link clicks
    document.querySelectorAll('.custom-pagination a').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    });

    // Clear filters button
    const clearBtn = document.querySelector('.btn-secondary');
    if (clearBtn) {
        clearBtn.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    }

    // Disable bedrooms and bathrooms when Land category is selected
    const categorySelect = document.querySelector('#id_category');
    const bedroomsInput = document.querySelector('#id_bedrooms');
    const bathroomsInput = document.querySelector('#id_bathrooms');

    if (!categorySelect || !bedroomsInput || !bathroomsInput) {
        console.error('Missing fields: category, bedrooms, or bathrooms');
        return;
    }

    function toggleFields() {
        const selectedText = categorySelect.options[categorySelect.selectedIndex].text.trim().toLowerCase();
        const selectedValue = categorySelect.value.trim().toLowerCase();

        if (selectedText === 'land' || selectedValue === 'land') {
            bedroomsInput.disabled = true;
            bathroomsInput.disabled = true;
            bedroomsInput.value = '';
            bathroomsInput.value = '';
        } else {
            bedroomsInput.disabled = false;
            bathroomsInput.disabled = false;
        }
    }

    // Initial check on page load
    toggleFields();

    // Check on change
    categorySelect.addEventListener('change', toggleFields);
});
