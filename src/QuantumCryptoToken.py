import random

def generate_key(bits):
    return [random.choice([0, 1]) for _ in range(bits)]

def encode_bits(bits, bases):
    encoded = []
    for bit, base in zip(bits, bases):
        if base == 0:  # Use standard basis
            encoded.append(bit)
        else:  # Use Hadamard basis
            encoded.append(random.choice([0, 1]))  # Encode randomly
    return encoded

def measure_bits(bits, bases):
    return [bit if base == 0 else random.choice([0, 1]) for bit, base in zip(bits, bases)]

def compare_bases(bases1, bases2):
    return [i for i in range(len(bases1)) if bases1[i] == bases2[i]]

def remove_indices(lst, indices):
    return [lst[i] for i in range(len(lst)) if i not in indices]

def bb84_key_exchange(num_bits):
    alice_bases = generate_key(num_bits)
    alice_key = generate_key(num_bits)
    alice_encoded = encode_bits(alice_key, alice_bases)
    
    bob_bases = generate_key(num_bits)
    bob_measurements = measure_bits(alice_encoded, bob_bases)
    bob_key = [bob_measurements[i] for i in range(len(bob_measurements)) if alice_bases[i] == bob_bases[i]]
    
    return alice_key, bob_key

def generateToken(num_bits):
    alice_key, _ = bb84_key_exchange(num_bits)
    k=''
    for i in alice_key:
        k+=str(i)
    return k
