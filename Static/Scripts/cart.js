$('.add-to-cart').on('click', function () {
    var productId = $(this).data('product-id');
    var productName = $(this).data('product-name');
    var productPrice = $(this).data('product-price');
    $.post('/add_to_cart', {
        product_id: productId,
        product_name: productName,
        price_unitary: productPrice
    }, function (data) {
        if (!data.success) {
            alert(data.message);
        }
    });
});

function fillModalWithCartItems() {
    $.get('/get_cart_items', function (data) {
        var modalContent = $('modal-content');
        modalContent.empty();  // Clear the modal content

        for (var productId in data) {
            var item = data[productId];
            var itemElement = `
          <div class="item">
            <h5>${item.product_name}</h5>
            <p>Quantity: ${item.quantity}</p>
            <p>Unit Price: ${item.price_unitary}</p>
          </div>
        `;
            modalContent.append(itemElement);
        }
    });
}

// Call the function when the modal is about to be shown
$('modal-2').on('show.bs.modal', fillModalWithCartItems);