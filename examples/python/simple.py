#!/usr/bin/env python3
"""
Test script for SLCAN connection to CAN bus
Connects to CAN bus at 500K baud rate via COM47
"""

import can
import time
import sys
from typing import Optional

def setup_slcan_bus(port: str = "COM47", bitrate: int = 500000) -> Optional[can.BusABC]:
    """
    Setup SLCAN bus connection
    
    Args:
        port: Serial port (e.g., "COM47" on Windows, "/dev/ttyUSB0" on Linux)
        bitrate: CAN bus bitrate (e.g., 500000 for 500K)
    
    Returns:
        CAN bus instance or None if connection fails
    """
    try:
        # Create SLCAN bus instance
        bus = can.interface.Bus(
            interface='slcan',
            channel=port,
            bitrate=bitrate,
            timeout=1.0
        )
        print(f"Successfully connected to CAN bus on {port} at {bitrate} bps")
        return bus
    except Exception as e:
        print(f"Failed to connect to CAN bus: {e}")
        return None

def send_test_message(bus: can.BusABC, can_id: int = 0x123, data: bytes = b'\x01\x02\x03\x04') -> bool:
    """
    Send a test CAN message
    
    Args:
        bus: CAN bus instance
        can_id: CAN message ID
        data: Message data bytes
    
    Returns:
        True if message sent successfully, False otherwise
    """
    try:
        message = can.Message(
            arbitration_id=can_id,
            data=data,
            is_extended_id=False
        )
        bus.send(message)
        print(f"Sent message: ID=0x{can_id:03X}, Data={data.hex().upper()}")
        return True
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False

def receive_messages(bus: can.BusABC, timeout: float = 5.0) -> None:
    """
    Receive and display CAN messages
    
    Args:
        bus: CAN bus instance
        timeout: Timeout in seconds for receiving messages
    """
    print(f"Listening for CAN messages (timeout: {timeout}s)...")
    start_time = time.time()
    
    try:
        while (time.time() - start_time) < timeout:
            message = bus.recv(timeout=0.1)
            if message is not None:
                print(f"Received message: ID=0x{message.arbitration_id:03X}, "
                      f"DLC={message.dlc}, Data={message.data.hex().upper()}, "
                      f"Timestamp={message.timestamp:.3f}")
    except KeyboardInterrupt:
        print("\nReceiving stopped by user")
    except Exception as e:
        print(f"Error receiving messages: {e}")

def main():
    """Main test function"""
    print("SLCAN CAN Bus Test")
    print("==================")
    
    # Setup CAN bus connection
    bus = setup_slcan_bus("COM47", 500000)
    if bus is None:
        sys.exit(1)
    
    try:
        # Send a test message
        print("\n--- Sending Test Message ---")
        send_test_message(bus, 0x123, b'\x01\x02\x03\x04\x05\x06\x07\x08')
        
        # Wait a moment
        time.sleep(0.5)
        
        # Listen for messages
        print("\n--- Receiving Messages ---")
        receive_messages(bus, timeout=10.0)
        
        # Send another test message
        print("\n--- Sending Another Test Message ---")
        send_test_message(bus, 0x456, b'\xAA\xBB\xCC\xDD')
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        # Clean up
        try:
            bus.shutdown()
            print("\nCAN bus connection closed")
        except Exception as e:
            print(f"Error closing CAN bus: {e}")

if __name__ == "__main__":
    main()
  
