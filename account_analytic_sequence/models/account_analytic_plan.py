# Copyright 2026 BADEP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticPlan(models.Model):
    _inherit = "account.analytic.plan"

    sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Analytic Account Sequence",
        help="Sequence used to assign codes to analytic accounts in this plan.",
    )
