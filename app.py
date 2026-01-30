"""
Smart Energy Load Balancer - Backend API
Flask REST API for energy management system with ML predictions
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# System State
system_state = {
    'grid': {
        'status': 'Online',
        'load': 0,
        'maxCapacity': 10.0,  # kW
        'currentUsage': 0
    },
    'battery': {
        'charge': 75,  # percentage
        'capacity': 10.0,  # kWh
        'status': 'Charging',
        'charging': True
    },
    'solar': {
        'generation': 2.5,  # kW
        'efficiency': 85,
        'peakCapacity': 5.0
    },
    'devices': {
        'air_conditioner': {
            'name': 'Air Conditioner',
            'power': 2.5,
            'active': False,
            'priority': 2
        },
        'water_heater': {
            'name': 'Water Heater',
            'power': 1.5,
            'active': False,
            'priority': 1
        },
        'washing_machine': {
            'name': 'Washing Machine',
            'power': 1.0,
            'active': False,
            'priority': 1
        },
        'refrigerator': {
            'name': 'Refrigerator',
            'power': 0.5,
            'active': True,
            'priority': 3
        },
        'lighting': {
            'name': 'Lighting',
            'power': 0.3,
            'active': True,
            'priority': 3
        }
    },
    'totalPower': 0.8,
    'powerSource': 'Solar Power'
}

# Historical data for ML
historical_data = []


def calculate_total_power():
    """Calculate total power consumption from active devices"""
    total = 0
    for device in system_state['devices'].values():
        if device['active']:
            total += device['power']
    return total


def update_system_metrics():
    """Update all system metrics based on current state"""
    total_power = calculate_total_power()
    system_state['totalPower'] = total_power
    
    # Update grid load percentage
    system_state['grid']['load'] = min(100, (total_power / system_state['grid']['maxCapacity']) * 100)
    system_state['grid']['currentUsage'] = total_power
    
    # Determine primary power source
    solar_gen = system_state['solar']['generation']
    battery_charge = system_state['battery']['charge']
    
    if solar_gen >= total_power:
        system_state['powerSource'] = 'Solar Power'
    elif solar_gen + (battery_charge * 0.1) >= total_power and battery_charge > 20:
        system_state['powerSource'] = 'Solar + Battery'
    else:
        system_state['powerSource'] = 'Grid Power'
    
    # Update battery status
    if solar_gen > total_power:
        system_state['battery']['charging'] = True
        system_state['battery']['status'] = 'Charging'
        system_state['battery']['charge'] = min(100, system_state['battery']['charge'] + 0.5)
    elif solar_gen < total_power and battery_charge > 20:
        system_state['battery']['charging'] = False
        system_state['battery']['status'] = 'Discharging'
        system_state['battery']['charge'] = max(0, system_state['battery']['charge'] - 0.3)
    else:
        system_state['battery']['status'] = 'Idle'
    
    # Auto load balancing - shed load if grid overloaded
    if system_state['grid']['load'] > 85:
        auto_load_shedding()
    
    return system_state


def auto_load_shedding():
    """Automatically turn off low-priority devices during overload"""
    # Sort devices by priority (lower number = lower priority)
    active_devices = [(key, device) for key, device in system_state['devices'].items() 
                      if device['active']]
    active_devices.sort(key=lambda x: x[1]['priority'])
    
    if active_devices:
        device_key, device = active_devices[0]
        system_state['devices'][device_key]['active'] = False
        print(f"⚠️ Load shedding: {device['name']} turned off (Grid overload)")


def generate_ml_prediction():
    """Generate ML-based demand predictions using simple forecasting"""
    current_hour = datetime.now().hour
    
    # Simulate demand prediction for next 24 hours
    predictions = []
    for i in range(24):
        hour = (current_hour + i) % 24
        
        # Base load varies by time of day
        if 6 <= hour <= 9 or 17 <= hour <= 20:
            base_load = 3.5 + random.uniform(-0.5, 0.5)  # Peak hours
        elif 10 <= hour <= 16:
            base_load = 2.5 + random.uniform(-0.4, 0.4)  # Day
        else:
            base_load = 1.5 + random.uniform(-0.3, 0.3)  # Night
        
        predictions.append(base_load)
    
    return {
        'nextHour': predictions[0],
        'peak': max(predictions),
        'average': sum(predictions) / len(predictions),
        'confidence': random.randint(88, 96),
        'forecast': predictions[:12]  # Next 12 hours
    }


def simulate_solar_variation():
    """Simulate realistic solar generation changes"""
    hour = datetime.now().hour
    
    # Solar only generates during daylight hours
    if 6 <= hour <= 18:
        # Peak generation at noon
        time_factor = 1 - abs(hour - 12) / 6
        base_generation = system_state['solar']['peakCapacity'] * time_factor
        variation = random.uniform(-0.3, 0.3)
        generation = max(0, min(system_state['solar']['peakCapacity'], base_generation + variation))
    else:
        generation = 0
    
    system_state['solar']['generation'] = generation
    system_state['solar']['efficiency'] = int((generation / system_state['solar']['peakCapacity']) * 100)


# API Routes

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current system state"""
    update_system_metrics()
    return jsonify(system_state)


@app.route('/api/device/<device_id>', methods=['POST'])
def toggle_device(device_id):
    """Toggle device on/off"""
    if device_id not in system_state['devices']:
        return jsonify({'success': False, 'error': 'Device not found'}), 404
    
    data = request.json
    system_state['devices'][device_id]['active'] = data.get('active', False)
    update_system_metrics()
    
    return jsonify({
        'success': True,
        'device': device_id,
        'active': system_state['devices'][device_id]['active'],
        'totalPower': system_state['totalPower']
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Run ML prediction model"""
    predictions = generate_ml_prediction()
    
    return jsonify({
        'success': True,
        'predictions': predictions,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Simulate system changes (solar variation, battery dynamics)"""
    simulate_solar_variation()
    update_system_metrics()
    
    return jsonify({
        'success': True,
        'state': system_state
    })


@app.route('/api/balance', methods=['POST'])
def balance_load():
    """Manually trigger load balancing"""
    update_system_metrics()
    
    return jsonify({
        'success': True,
        'message': 'Load balancing completed',
        'state': system_state
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get historical data"""
    return jsonify({
        'success': True,
        'data': historical_data[-100:]  # Last 100 entries
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    total_power = calculate_total_power()
    
    stats = {
        'currentLoad': total_power,
        'gridLoad': system_state['grid']['load'],
        'solarGeneration': system_state['solar']['generation'],
        'batteryCharge': system_state['battery']['charge'],
        'activeDevices': sum(1 for d in system_state['devices'].values() if d['active']),
        'totalDevices': len(system_state['devices']),
        'efficiency': (system_state['solar']['generation'] / total_power * 100) if total_power > 0 else 0,
        'renewablePercentage': min(100, (system_state['solar']['generation'] / total_power * 100)) if total_power > 0 else 0
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Reset system to default state"""
    # Reset devices
    for device_id in system_state['devices']:
        if device_id in ['refrigerator', 'lighting']:
            system_state['devices'][device_id]['active'] = True
        else:
            system_state['devices'][device_id]['active'] = False
    
    # Reset battery
    system_state['battery']['charge'] = 75
    system_state['battery']['status'] = 'Charging'
    
    # Reset solar
    system_state['solar']['generation'] = 2.5
    system_state['solar']['efficiency'] = 50
    
    update_system_metrics()
    
    return jsonify({
        'success': True,
        'message': 'System reset to default state',
        'state': system_state
    })


@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'name': 'Smart Energy Load Balancer API',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            'GET /api/state': 'Get current system state',
            'POST /api/device/<id>': 'Toggle device on/off',
            'POST /api/predict': 'Run ML prediction',
            'POST /api/simulate': 'Simulate system changes',
            'POST /api/balance': 'Trigger load balancing',
            'GET /api/history': 'Get historical data',
            'GET /api/stats': 'Get system statistics',
            'POST /api/reset': 'Reset system to default'
        }
    })


# Error Handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🔋 SMART ENERGY LOAD BALANCER - Backend API")
    print("="*60)
    print("\n✅ Server starting...")
    print("📡 API available at: http://localhost:5000")
    print("📊 Endpoints:")
    print("   - GET  /api/state      (System state)")
    print("   - POST /api/device/:id (Toggle device)")
    print("   - POST /api/predict    (ML prediction)")
    print("   - POST /api/simulate   (Simulate changes)")
    print("   - GET  /api/stats      (Statistics)")
    print("\n⚡ Press CTRL+C to stop\n")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)