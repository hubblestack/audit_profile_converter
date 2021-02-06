from module_handler.audit.grep import Grep
from module_handler.audit.sysctl import Sysctl
from module_handler.audit.pkg import Pkg
from module_handler.audit.systemctl import Systemctl
from module_handler.audit.stat import Stat
from module_handler.audit.misc import Misc
from module_handler.audit.service import Service
from module_handler.audit.winsecedit import WinSecedit
from module_handler.audit.winreg import WinReg
from module_handler.audit.winpkg import WinPkg
from module_handler.audit.winfirewall import WinFirewall
from module_handler.audit.winauditpol import WinAuditPol
from module_handler.audit.fdg_connector import FdgConnector

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
    elif module_name == 'win_auditpol':
        handler = WinAuditPol
    elif module_name == 'fdg':
        handler = FdgConnector

    if handler:
        return handler(report_handler, module_name, module_block)
    return None
