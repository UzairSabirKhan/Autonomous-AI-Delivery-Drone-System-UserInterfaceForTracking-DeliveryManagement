from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Utility Functions for File-Based Database
def read_data(file_name):
    with open(f'AI-Delivery/{file_name}', 'r') as file:
        return json.load(file)

def write_data(file_name, data):
    with open(f'AI-Delivery/{file_name}', 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/')
def home():
    return "Hello"


# ---------------- Delivery Management System Module ----------------

@app.route('/assign-delivery', methods=['POST'])
def assign_delivery():
    """
    Assigns a delivery to an available drone.
    Request JSON: { "deliveryID": int, "customerID": int, "packageDetails": dict }
    """
    data = request.json  # Ensure JSON decoding

    drones = read_data('drones.json')
    deliveries = read_data('deliveries.json')

    # Find an available drone
    available_drone = next((drone for drone in drones if drone['status'] == "Idle"), None)
    if not available_drone:
        return jsonify({"message": "No available drones"}), 400

    # Create the new delivery
    new_delivery = {
        "deliveryID": data['deliveryID'],
        "customerID": data['customerID'],
        "droneID": available_drone['droneID'],
        "status": "In Transit",
        "packageDetails": data['packageDetails']
    }
    deliveries.append(new_delivery)
    available_drone['status'] = "In Transit"

    # Update data
    write_data('deliveries.json', deliveries)
    write_data('drones.json', drones)

    return jsonify({"message": "Delivery assigned successfully", "droneID": available_drone['droneID']}), 201

@app.route('/update-delivery-status/<int:deliveryID>', methods=['POST'])
def update_delivery_status(deliveryID):
    # Updates the status of a delivery.
    data = request.json
    deliveries = read_data('deliveries.json')

    # Find the delivery
    delivery = next((d for d in deliveries if int(d['deliveryID']) == deliveryID), None)
    if not delivery:
        return jsonify({"message": "Delivery not found"}), 404

    # Update the status
    delivery['status'] = data['status']
    if data['status'] in ["Delivered", "Failed"]:
        # Set the drone back to "Idle"
        drones = read_data('drones.json')
        drone = next((d for d in drones if d['droneID'] == delivery['droneID']), None)
        if drone:
            drone['status'] = "Idle"
            write_data('drones.json', drones)

    write_data('deliveries.json', deliveries)
    return jsonify({"message": f"Delivery status updated to {data['status']}"}), 200

@app.route('/list-deliveries', methods=['GET'])
def list_deliveries():
    """
    Lists all deliveries and their current statuses.
    """
    deliveries = read_data('deliveries.json')
    return jsonify(deliveries)

# ---------------- User Interface for Tracking Module ----------------

@app.route('/drone/location', methods=['GET'])
def get_drone_location():
    # Retrieves the real-time location of all drones.
    drones = read_data('drones.json')
    return jsonify(drones)

@app.route('/delivery/status/<int:customerID>', methods=['GET'])
def get_delivery_status(customerID):
    
    # Fetches the delivery status for a specific customer.
    deliveries = read_data('deliveries.json')
    delivery = next((d for d in deliveries if int(d['customerID']) == customerID), None)
    if delivery:
        droneID = delivery['droneID']
        drones = read_data('drones.json')
        drone = next((d for d in drones if int(d['droneID']) == droneID), None)
        return jsonify({
            "status": delivery['status'],
            "location": drone['location'] if drone else "Location unavailable"
        })
    return jsonify({"message": "Delivery not found"}), 404




@app.route('/simulate/drone/<int:droneID>', methods=['POST'])
def update_drone_location(droneID):
    """
    Simulates a drone's location update.
    Request JSON: { "location": { "lat": float, "lng": float } }
    """
    data = request.json
    drones = read_data('drones.json')
    for drone in drones:
        if drone['droneID'] == droneID:
            drone['location'] = data['location']
            write_data('drones.json', drones)
            return jsonify({"message": "Drone location updated"})
    return jsonify({"message": "Drone not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
