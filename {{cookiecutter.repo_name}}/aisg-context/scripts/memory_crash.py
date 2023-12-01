# Set the memory accordingly; this is to crash an 8G deployment to see if it spins a new pod
import torch

# Set the size of the tensor to consume memory
tensor_size_gb = 10

# Convert the size to bytes
tensor_size_bytes = tensor_size_gb * 1024 * 1024 * 1024

# Create a tensor of zeros with the specified size
tensor = torch.zeros(int(tensor_size_bytes / 4))

# Perform some operations to ensure the tensor is allocated in memory
result = tensor.sum()

# Print the result
print(result)
