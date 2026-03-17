import torch
import sys

def check_gpu():
    print(f"--- Environment Check ---")
    print(f"Python Version: {sys.version}")
    print(f"PyTorch Version: {torch.__version__}")
    
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_available}")
    
    # Check for build info
    print(f"CUDA Build Version: {torch.version.cuda}")
    
    if cuda_available:
        print(f"\n--- GPU Details ---")
        device_count = torch.cuda.device_count()
        print(f"Number of GPUs: {device_count}")
        for i in range(device_count):
            print(f"Device {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Memory allocated: {torch.cuda.memory_allocated(i) / 1024**2:.2f} MB")
            print(f"  Memory reserved: {torch.cuda.memory_reserved(i) / 1024**2:.2f} MB")
    else:
        print("\n--- Why is CUDA NOT available? ---")
        if torch.version.cuda is None:
            print("Reason: You likely installed the CPU-only version of PyTorch.")
            print("Fix: Run 'pip uninstall torch' then install the CUDA version from pytorch.org.")
        else:
            print("Reason: PyTorch has CUDA support, but can't talk to your GPU.")
            print("Check: Ensure you have recent NVIDIA drivers and the CUDA Toolkit installed.")

if __name__ == "__main__":
    try:
        check_gpu()
    except Exception as e:
        print(f"Error during check: {e}")
