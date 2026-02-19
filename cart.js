/*document.addEventListener("DOMContentLoaded", function () {

    const cartRows = document.querySelectorAll('.cart-row');
    const totalEl = document.getElementById('total');
    const deliveryRadios = document.querySelectorAll('input[name="delivery"]');

    function calculateTotal() {
        let total = 0;

        cartRows.forEach(row => {
            const checkbox = row.querySelector('.cart-check');
            const qty = parseInt(row.querySelector('.qty').value);
            const price = parseInt(row.dataset.price);

            if (checkbox.checked) {
                total += price * qty;
            }
        });

        const deliveryFee = parseInt(
            document.querySelector('input[name="delivery"]:checked').value
        );

        total += deliveryFee;
        totalEl.textContent = `R${total}`;
    }

    cartRows.forEach(row => {
        const plus = row.querySelector('.plus');
        const minus = row.querySelector('.minus');
        const qty = row.querySelector('.qty');
        const checkbox = row.querySelector('.cart-check');

        plus.addEventListener('click', () => {
            qty.value++;
            if (checkbox.checked) calculateTotal();
        });

        minus.addEventListener('click', () => {
            qty.value = Math.max(1, qty.value - 1);
            if (checkbox.checked) calculateTotal();
        });

        checkbox.addEventListener('change', calculateTotal);
        qty.addEventListener('input', calculateTotal);
    });

    deliveryRadios.forEach(radio =>
        radio.addEventListener('change', calculateTotal)
    );

});*/

document.addEventListener("DOMContentLoaded", () => {

    const deliveryRadios = document.querySelectorAll("input[name='delivery_option']");
    const form = document.querySelector("form");
    const cards = document.querySelectorAll(".cart-card");
    const totalText = document.getElementById("total");
    const checkoutBtn = document.querySelector(".checkout-btn");
    let deliveryFee = 0;
    const selectedOption = document.querySelector("input[name='delivery_option']:checked");

    if (selectedOption && selectedOption.value === "delivery") {
    deliveryFee = 20;
    }

    total += deliveryFee;


    // Calculate total function
    function calculateTotal() {
        let total = 0;
        let hasItems = false;

        cards.forEach(card => {
            const checkbox = card.querySelector(".item-checkbox");
            const qtyInput = card.querySelector(".quantity");
            const price = parseFloat(card.dataset.price);

            if (checkbox.checked) {
                hasItems = true;
                total += price * parseInt(qtyInput.value);
            }
        });

        // Add delivery fee if selected
        let deliveryFee = 0;
        const selectedDelivery = document.querySelector("input[name='delivery_option']:checked");
        if (selectedDelivery && selectedDelivery.value === "delivery") {
            deliveryFee = 20;
        }
        total += deliveryFee;

        if (!hasItems) {
            totalText.textContent = "Your cart is empty";
            checkoutBtn.disabled = true;
        } else {
            totalText.textContent = `R${total}`;
            checkoutBtn.disabled = false;
        }
    }

    // Enable/disable quantity input based on checkbox
    cards.forEach(card => {
        const checkbox = card.querySelector(".item-checkbox");
        const qtyInput = card.querySelector(".quantity");
        const minusBtn = card.querySelector(".minus");
        const plusBtn = card.querySelector(".plus");

        checkbox.addEventListener("change", () => {
            const enabled = checkbox.checked;
            qtyInput.disabled = !enabled;
            minusBtn.disabled = !enabled;
            plusBtn.disabled = !enabled;
            calculateTotal();
        });

        plusBtn.addEventListener("click", () => {
            qtyInput.value++;
            calculateTotal();
        });

        minusBtn.addEventListener("click", () => {
            if (qtyInput.value > 1) {
                qtyInput.value--;
                calculateTotal();
            }
        });

        qtyInput.addEventListener("input", calculateTotal);
    });

    // Add event listener for delivery option changes
    deliveryRadios.forEach(radio => {
        radio.addEventListener("change", calculateTotal);
    });

    // Prevent form submission if no item is selected
    form.addEventListener("submit", (e) => {
        const anyChecked = Array.from(document.querySelectorAll(".item-checkbox")).some(cb => cb.checked);
        if (!anyChecked) {
            e.preventDefault();
            alert("Please select at least one item before checkout!");
        }
    });

    // Initial total calculation
    calculateTotal();

});



