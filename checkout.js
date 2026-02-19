const deliveryRadio = document.querySelector('input[value="delivery"]');
const collectionRadio = document.querySelector('input[value="collection"]');
const addressDiv = document.getElementById('delivery_address');
const addressInput = addressDiv.querySelector("input[name='address']");

function toggleAddress() {
    if (deliveryRadio.checked) {
        addressDiv.style.display = "block"
        addressInput.required = true;
    } else {
        addressDiv.style.display = "none";
        address.Input.required = false;
        addressInput.value = "";
    }
  }

deliveryRadio.addEventListener("change", toggleAddress);
collectionRadio.addEventListener("change", toggleAddress);

toggleAddress();


//deliveryRadio.addEventListener('change', () => addressDiv.style.display = 'block');
//collectionRadio.addEventListener('change', () => addressDiv.style.display = 'none');
