document.addEventListener('DOMContentLoaded',() => {
    document.querySelectorAll('.btn-delete').forEach(button =>{
        button.onclick = () => {
            if (!confirm('Are you sure you want to delete it?.')) {
                return false;
            }
        };
    });
});