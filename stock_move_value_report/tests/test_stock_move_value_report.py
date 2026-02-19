# Copyright 2025 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.base.tests.common import BaseCommon


class Test(BaseCommon):
    """
    Tests for stock_move_value_report.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pickings = cls.env["stock.picking"].search([], limit=100)
        cls.moves = cls.pickings.move_ids
        cls.move_lines = cls.moves.move_line_ids
        picking = cls.pickings[0]
        product = picking.move_ids[0].product_id
        cls.scrap = cls.env["stock.scrap"].create(
            {
                "product_id": product.id,
                "product_uom_id": product.uom_id.id,
            }
        )

    def _render_report(self, report_name, records):
        """
        Ensure rendering passes without errors
        """
        context = {
            **self.env.context,
            "active_ids": records.ids,
            "active_model": "stock.move",
        }
        self.env["ir.actions.report"].with_context(**context)._render_qweb_pdf(
            report_name, records.ids, data={"context": context}
        )

    def test_report_stock_move_line_value(self):
        report_name = "stock_move_value_report.report_stock_move_line_value"
        self.assertTrue(bool(self.move_lines))
        self._render_report(report_name, self.move_lines)

    def test_report_stock_move_value(self):
        report_name = "stock_move_value_report.report_stock_move_value"
        self.assertTrue(bool(self.moves))
        self._render_report(report_name, self.moves)

    def test_report_stock_picking_value(self):
        report_name = "stock_move_value_report.report_stock_picking_value"
        self.assertTrue(bool(self.pickings))
        self._render_report(report_name, self.pickings)

    def test_report_stock_scrap_value(self):
        report_name = "stock_move_value_report.report_stock_scrap_value"
        self.assertTrue(bool(self.scrap))
        self._render_report(report_name, self.scrap)
