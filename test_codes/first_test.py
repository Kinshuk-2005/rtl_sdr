from rtlsdr import RtlSdr
import numpy as np

def acquire_samples():
    """
    Configures the RTL-SDR dongle and reads samples.
    """
    sdr = RtlSdr()

    # Configure device settings
    sdr.sample_rate = 2.048e6  # 2.048 MS/s
    sdr.center_freq = 70e6   # 70 MHz
    sdr.freq_correction = 60 # PPM
    sdr.gain = 'auto'        # Set gain to automatic

    try:
        # Read a specific number of samples (must be a power of two, e.g., 512, 1024, 2048...)
        # Using a higher number like 1024 or higher powers of two is recommended for stability
        num_samples = 1024
        samples = sdr.read_samples(num_samples)

        print(f"Read {len(samples)} samples successfully.")
        print(f"Sample data type: {type(samples)}")
        print(f"First 10 samples: {samples[:10]}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the device
        sdr.close()
        print("SDR device closed.")

if __name__ == "__main__":
    acquire_samples()
