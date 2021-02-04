from module_handler.grep import Grep
from module_handler.sysctl import Sysctl
from module_handler.pkg import Pkg
from module_handler.systemctl import Systemctl
from module_handler.stat import Stat
from module_handler.misc import Misc
from module_handler.service import Service
from module_handler.winsecedit import WinSecedit
from module_handler.winreg import WinReg
from module_handler.winpkg import WinPkg
from module_handler.winfirewall import WinFirewall

def get_module_handler(report_handler, module_name, module_block):
    handler = None
    if module_name == 'grep':
        handler = Grep
    elif module_name == 'sysctl':
        handler = Sysctl
    elif module_name == 'pkg':
        handler = Pkg
    elif module_name == 'systemctl':
        handler = Systemctl
    elif module_name == 'stat':
        handler = Stat
    elif module_name == 'misc':
        handler = Misc
    elif module_name == 'service':
        handler = Service
    elif module_name == 'win_secedit':
        handler = WinSecedit
    elif module_name == 'win_reg':
        handler = WinReg
    elif module_name == 'win_pkg':
        handler = WinPkg
    elif module_name == 'win_firewall':
        handler = WinFirewall

    if handler:
        return handler(report_handler, module_name, module_block)
    return None
