import struct

def is_64bit_dll(file_path):
    with open(file_path, 'rb') as f:
        f.seek(60)  # PE header offset
        pe_offset = struct.unpack('<L', f.read(4))[0]
        f.seek(pe_offset + 4)  # Machine type offset
        machine = struct.unpack('<H', f.read(2))[0]
        return machine == 0x8664  # 0x8664 is x64, 0x014C is x86

dll_path = r'C:\Users\Amir Yeganeh\Desktop\Amir\Sakhtar\straight.dll'

print("Is 64-bit DLL:", is_64bit_dll(dll_path))
