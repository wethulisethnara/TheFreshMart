document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('item-modal');
    const modalBody = document.getElementById('modal-body');
    const closeBtn = document.querySelector('.close-btn');

    // Close modal
    closeBtn.onclick = () => {
        modal.style.display = 'none';
        modalBody.innerHTML = ''; // Clear modal content
    };

    // Handle button clicks
    document.querySelectorAll('.view-btn, .update-btn, .delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.getAttribute('data-item-id');
            modal.style.display = 'block';

            if (button.classList.contains('view-btn')) {
                // Fetch details for the "view" action
                fetch(`/app/item/${itemId}/`)
                    .then(response => response.text())
                    .then(html => {
                        modalBody.innerHTML = html;
                    });
                } else if (button.classList.contains('update-btn')) {
                    // Fetch the update form dynamically
                    fetch(`/app/update/${itemId}/`)
                        .then(response => response.text())
                        .then(html => {
                            modalBody.innerHTML = html;
                
                            // Attach form submission logic to the dynamically loaded form
                            const updateForm = modalBody.querySelector('form');
                            updateForm.addEventListener('submit', (event) => {
                                event.preventDefault(); // Prevent default form submission
                
                                const formData = new FormData(updateForm);
                
                                fetch(updateForm.action, {
                                    method: 'POST',
                                    body: formData,
                                })
                                    .then((response) => response.json())
                                    .then((data) => {
                                        if (data.success) {
                                            // Display a success message
                                            alert(data.message);
                
                                            // Close the modal
                                            modal.style.display = 'none';
                                            modalBody.innerHTML = '';
                
                                            // Update the table data dynamically
                                            const updatedRow = document.querySelector(
                                                `tr[data-item-id="${itemId}"]`
                                            );
                                            if (updatedRow) {
                                                updatedRow.querySelector('.name-cell').textContent =
                                                    data.updatedItem.name;
                                                updatedRow.querySelector('.description-cell').textContent =
                                                    `${data.updatedItem.description}`;
                                                updatedRow.querySelector('.price-cell').textContent =
                                                    `${data.updatedItem.price}`;
                                                updatedRow.querySelector('.image-cell img').src =
                                                    data.updatedItem.image_url; 
                                                updatedRow.querySelector('.catergory-cell').textContent =
                                                    `${data.updatedItem.catergory}`;
                                                updatedRow.querySelector('.unit-cell').textContent =
                                                    `${data.updatedItem.unit}`;
                                            }
                                        } else {
                                            // Display an error message (if any)
                                            alert('Failed to update the item. Please try again.');
                                        }
                                    })
                                    .catch((error) => {
                                        console.error('Error updating item:', error);
                                    });
                            });
                        });
                    } else if (button.classList.contains('delete-btn')) {
                        // Fetch delete confirmation modal content
                        fetch(`/app/delete-confirm/${itemId}/`)
                            .then(response => response.text())
                            .then(html => {
                                modalBody.innerHTML = html;
                    
                                // Add event listener to the delete confirmation form
                                const deleteForm = modalBody.querySelector('form');
                                deleteForm.addEventListener('submit', (event) => {
                                    event.preventDefault();
                    
                                    fetch(deleteForm.action, {
                                        method: 'POST',
                                        body: new FormData(deleteForm),
                                    })
                                        .then((response) => response.json())
                                        .then((data) => {
                                            if (data.success) {
                                                alert(data.message);
                    
                                                // Close the modal
                                                modal.style.display = 'none';
                                                modalBody.innerHTML = '';
                    
                                                // Remove the deleted item from the table
                                                const deletedRow = document.querySelector(
                                                    `tr[data-item-id="${itemId}"]`
                                                );
                                                if (deletedRow) {
                                                    deletedRow.remove();
                                                }
                    
                                                // Optionally, reload the page or show a success banner
                                                const successBanner = document.createElement('div');
                                                successBanner.textContent = data.message;
                                                successBanner.style.cssText = `
                                                    background-color: green;
                                                    color: white;
                                                    text-align: center;
                                                    padding: 10px;
                                                    margin: 10px 0;
                                                    border-radius: 5px;
                                                `;
                                                document.body.prepend(successBanner);
                    
                                                // Remove the banner after a few seconds
                                                setTimeout(() => {
                                                    successBanner.remove();
                                                }, 3000);
                                            } else {
                                                alert('Failed to delete the item. Please try again.');
                                            }
                                        })
                                        .catch((error) => {
                                            console.error('Error deleting item:', error);
                                        });
                                });
                            });
                    }                    
        });
    });

    // Close modal on outside click
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
            modalBody.innerHTML = '';
        }
    };
});
