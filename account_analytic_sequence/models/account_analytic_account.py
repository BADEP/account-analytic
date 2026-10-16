# Copyright 2017 ACSONE SA/NV
# Copyright 2020 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    code = fields.Char(
        copy=False,
    )

    _code_company_uniq = models.Constraint(
        "UNIQUE(code, company_id)",
        "Reference must be unique per Company!",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code"):
                plan = self.env["account.analytic.plan"].browse(vals.get("plan_id"))
                vals["code"] = self._default_code(plan)
        return super().create(vals_list)

    @api.model
    def _default_code(self, plan=None):
        if plan and plan.sequence_id:
            return plan.sequence_id.next_by_id()
        return self.env["ir.sequence"].next_by_code("account.analytic.account.code")

    def action_resequence(self):
        for account in self:
            account.code = account._default_code(account.plan_id)
        return True

    @api.model
    def _assign_default_codes(self):
        for aaa in self.with_context(active_test=False).search([("code", "=", False)]):
            aaa.code = self._default_code(aaa.plan_id)
