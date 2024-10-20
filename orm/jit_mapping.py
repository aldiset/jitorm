import llvmlite.binding as llvm
import llvmlite.ir as ir

# Inisialisasi LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

jit_cache = {}

def create_jit_function(cls):
    module = ir.Module(name="jit_mapping_module")

    func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
    function = ir.Function(module, func_type, name="map_to_instance")

    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Membangun pemetaan dinamis
    for i, field_name in enumerate(cls._fields.keys()):
        # Ambil elemen data dari argumen kedua (tuple) berdasarkan indeks
        data_ptr = builder.gep(function.args[1], [ir.Constant(ir.IntType(32), i)])
        
        # data_ptr adalah pointer ke elemen, kita perlu mengaksesnya sebagai pointer sesuai tipe datanya
        field_type = cls._fields[field_name].__class__.__name__

        if field_type == "IntegerField":
            # Pemetaan integer: Asumsikan bahwa integer disimpan sebagai int32
            int_ptr = builder.bitcast(data_ptr, ir.IntType(32).as_pointer())  # Cast ke pointer integer 32-bit
            int_val = builder.load(int_ptr)  # Load nilai integer dari pointer
            # Di sini kita akan menyimpan integer ke objek Python

        elif field_type == "StringField":
            # Pemetaan string, alokasi pointer untuk string
            string_ptr = builder.bitcast(data_ptr, ir.IntType(8).as_pointer())  # Bitcast pointer untuk string
            # String diperlakukan sebagai pointer (dapat dimanipulasi di sini)

        elif field_type == "BooleanField":
            # Pemetaan boolean: Asumsikan boolean disimpan sebagai integer 1-bit (0 atau 1)
            bool_ptr = builder.bitcast(data_ptr, ir.IntType(1).as_pointer())  # Cast ke pointer boolean 1-bit
            bool_val = builder.load(bool_ptr)  # Load nilai boolean dari pointer
            # Di sini kita bisa memetakan bool_val ke field boolean di model

        else:
            raise TypeError(f"Unsupported field type: {field_type}")

    # Kembalikan kontrol ke fungsi caller setelah pemetaan selesai
    builder.ret_void()

    return module

def compile_and_run_jit(cls, data):
    # Cek apakah modul untuk class ini sudah ada di cache
    if cls in jit_cache:
        engine = jit_cache[cls]
    else:
        # Jika belum ada, buat modul JIT dan kompilasi
        module = create_jit_function(cls)
        llvm_ir = str(module)

        # Buat mesin eksekusi LLVM
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

        # Parsing modul IR untuk mendapatkan LLVMModuleRef
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()

        # Optimasi LLVM menggunakan pass manager
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 3  # Level optimasi maksimum
        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)
        pm.run(mod)  # Gunakan 'mod' yang sudah diparse, bukan 'module' dari llvmlite.ir

        # Kompilasi IR menjadi kode mesin
        engine.add_module(mod)
        engine.finalize_object()
        engine.run_static_constructors()

        # Simpan engine ke dalam cache untuk reusability
        jit_cache[cls] = engine

    return cls(**dict(zip(cls._fields.keys(), data)))

def map_to_instance(cls, data):
    return compile_and_run_jit(cls, data)
