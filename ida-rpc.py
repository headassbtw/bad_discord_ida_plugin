import idaapi
import ida_ida
import time
import os
import pypresence

client_id = 1274916891609272331

def long_arch(arch):
    comp = arch.lower()
    if comp == "ppc":
        return "PowerPC"
    if comp == "ppcl":
        return "PowerPC (Little Endian)"
    if comp == "mipsl":
        return "MIPS"
    if comp == "mipsb":
        return "MIPS (Big-Endian)"
    if comp == "r5900l":
        return "MIPS R5900"
    if comp == "r5900b":
        return "MIPS R5900 (Big-Endian???)"
    if comp == "psp":
        return "MIPS R4000"
    if comp == "x86" or comp == "athlon" or comp == "8086":
        return "x86"
    if comp == "metapc":
        return "x86 (probably)"
    if comp == "arm":
        return "ARM"
    if comp == "armb":
        return "ARM (Big-Endian)"
    else:
        return arch
def img_arch(arch):
    comp = arch.lower()
    if comp == "ppc" or comp == "ppcl":
        return "ppc"
    if comp == "x86" or comp == "metapc" or comp == "athlon" or comp == "8086":
        return "x86"
    if comp == "r5900l" or comp == "r5900b" or comp == "psp" or comp == "mipsl" or comp == "mipsb":
        return "mips"
    if comp == "arm" or comp == "armb":
        return "arm"

class discord_plugin_t(idaapi.plugin_t):
    running = True
    flags = idaapi.PLUGIN_HIDE
    comment = ""
    help = ""
    wanted_name = "Discord Rich Presence"
    wanted_hotkey = ""
    RPC = pypresence.Presence(client_id)

    def init(self):
        try:
            self.RPC.connect()
        except pypresence.exceptions.DiscordNotFound:
            print("Discord client not detected. Make sure Discord is running.")
            return idaapi.PLUGIN_SKIP
        print("Discord connected")
        self.run_rpc()
        return idaapi.PLUGIN_KEEP

    def run_rpc(self):
        db_path = idaapi.get_input_file_path()
        processor_name = ida_ida.inf_get_procname()
        activity = {
            'details': f"Reversing {os.path.basename(db_path)}",
            #'state': f"{processor_name.lower()} / {long_arch(processor_name)}",
            'small_image': 'appico',
            'small_text': "IDA Pro (cracked)",
            'large_image': img_arch(processor_name),
            'large_text': long_arch(processor_name),
            'start': int(time.time())
        }

        self.RPC.update(**activity)

    def run(self, arg):
        pass

    def term(self):
        self.RPC.close()
        print("Discord Disconnected")

def PLUGIN_ENTRY():
    return discord_plugin_t()
