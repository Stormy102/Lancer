from core import ModuleProvider, ArgHandler, Loot
from core.reports.JSONReport import JSONReport
from core.reports.TerminalReport import TerminalReport

ArgHandler.parse_arguments(["-T", "127.0.0.1", "-v"])

ModuleProvider.main()

report = JSONReport()
report.generate_report(Loot.loot)

report = TerminalReport()
report.generate_report(Loot.loot)
