document.getElementById('assignDeliveryBtn').addEventListener('click', showAssignDeliveryForm);
document.getElementById('updateStatusBtn').addEventListener('click', showUpdateStatusForm);
document.getElementById('listDeliveriesBtn').addEventListener('click', listDeliveries);
document.getElementById('trackDeliveryBtn').addEventListener('click', showTrackDeliveryForm);

const baseUrl = 'http://127.0.0.1:5000';

function showAssignDeliveryForm() {
    document.getElementById('content').innerHTML = `
        <h2>Assign Delivery</h2>
        <form id="assignForm">
            <input type="number" id="deliveryID" placeholder="Delivery ID" required />
            <input type="number" id="customerID" placeholder="Customer ID" required />
            <textarea id="packageDetails" placeholder="Package Details" required></textarea>
            <button type="submit">Assign Delivery</button>
        </form>
        <div id="result"></div>
    `;
    document.getElementById('assignForm').onsubmit = handleAssignDelivery;
}

async function handleAssignDelivery(event) {
    event.preventDefault();
    const deliveryID = document.getElementById('deliveryID').value;
    const customerID = document.getElementById('customerID').value;
    const packageDetails = document.getElementById('packageDetails').value;

    const response = await fetch(`${baseUrl}/assign-delivery`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deliveryID, customerID, packageDetails }),
    });
    const data = await response.json();
    console.log(data);
    document.getElementById('result').innerText = data.message;
}

function showUpdateStatusForm() {
    document.getElementById('content').innerHTML = `
        <h2>Update Delivery Status</h2>
        <form id="statusForm">
            <input type="number" id="statusDeliveryID" placeholder="Delivery ID" required />
            <input type="text" id="newStatus" placeholder="New Status (e.g., Delivered)" required />
            <button type="submit">Update Status</button>
        </form>
        <div id="result"></div>
    `;
    document.getElementById('statusForm').onsubmit = handleUpdateStatus;
}

async function handleUpdateStatus(event) {
    event.preventDefault();
    const deliveryID = document.getElementById('statusDeliveryID').value;
    const status = document.getElementById('newStatus').value;

    const response = await fetch(`${baseUrl}/update-delivery-status/${deliveryID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
    });
    const data = await response.json();
    document.getElementById('result').innerText = data.message;
}

async function listDeliveries() {
    const response = await fetch(`${baseUrl}/list-deliveries`);
    const deliveries = await response.json();
    let content = '<h2>All Deliveries</h2><ul>';
    deliveries.forEach(delivery => {
        content += `<li>
            Delivery ID: ${delivery.deliveryID}, Customer ID: ${delivery.customerID}, Status: ${delivery.status}
        </li>`;
    });
    content += '</ul>';
    document.getElementById('content').innerHTML = content;
}

function showTrackDeliveryForm() {
    document.getElementById('content').innerHTML = `
        <h2>Track Delivery</h2>
        <form id="trackForm">
            <input type="number" id="trackCustomerID" placeholder="Customer ID" required />
            <button type="submit">Track Delivery</button>
        </form>
        <div id="result"></div>
    `;
    document.getElementById('trackForm').onsubmit = handleTrackDelivery;
}

async function handleTrackDelivery(event) {
    event.preventDefault();
    const customerID = document.getElementById('trackCustomerID').value;

    const response = await fetch(`${baseUrl}/delivery/status/${customerID}`);
    const data = await response.json();
    document.getElementById('result').innerText = data.message || 
        `Status: ${data.status}, Location: Lat ${data.location.lat}, Lng ${data.location.lng}`;
}
