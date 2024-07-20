let currentPage = 1;
const itemsPerPage = 6;
// alert("assa");
function loadProducts(page) {
    // alert("Dsd");
    frappe.call({
        method: "perfect_theme.api.get_items",
        args: {
            page: page,
            items_per_page: itemsPerPage
        },
        callback: function(response) {
            let products = response.message;
            let container = document.getElementById("product-container");
            container.innerHTML = "";
            products.forEach(product => {
                container.innerHTML += `<div>${product.name}</div>`;
            });
        }
    });
}

function loadNext() {
    currentPage++;
    loadProducts(currentPage);
}

function loadPrevious() {
    if (currentPage > 1) {
        currentPage--;
        loadProducts(currentPage);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    loadProducts(currentPage);
});
