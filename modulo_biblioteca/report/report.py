from odoo import models, api

class ReporteLibro(models.AbstractModel):
    _name = "report.modulo_biblioteca.report_libros"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["bi.libro"].browse(docids)

        docargs = {
            "docs": docs,
            "other_valor": "Esto es valor X",
        }

        return docargs