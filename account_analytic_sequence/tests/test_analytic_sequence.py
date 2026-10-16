# Copyright 2017 ACSONE SA/NV
# Copyright 2020 Brainbean Apps (https://brainbeanapps.com)
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestAccountAnalyticSequence(BaseCommon):
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.analytic_account_obj = cls.env["account.analytic.account"]
        cls.plan = cls.env["account.analytic.plan"].create({"name": "Test plan"})
        cls.analytic = cls.analytic_account_obj.create(
            {"name": "aa", "partner_id": cls.partner.id, "plan_id": cls.plan.id}
        )

    def test_account_analytic_account_code(self):
        self.assertTrue(self.analytic.code, "Sequence not added")
        self.assertTrue(self.analytic.code.startswith("AA"))
        analytic2 = self.analytic_account_obj.create(
            {"name": "Test 2", "plan_id": self.plan.id, "code": "TEST"}
        )
        self.assertEqual(analytic2.code, "TEST")

    def test_plan_sequence_used(self):
        sequence = self.env["ir.sequence"].create(
            {
                "name": "Analytic account plan sequence",
                "code": "test.analytic.account.plan",
                "prefix": "PLAN/",
                "padding": 4,
                "company_id": False,
            }
        )
        self.plan.sequence_id = sequence

        analytic = self.analytic_account_obj.create(
            {"name": "Plan sequence account", "plan_id": self.plan.id}
        )

        self.assertEqual(analytic.code, "PLAN/0001")

    def test_resequence_uses_plan_sequence(self):
        sequence = self.env["ir.sequence"].create(
            {
                "name": "Analytic account resequence",
                "code": "test.analytic.account.resequence",
                "prefix": "NEXT/",
                "padding": 3,
                "company_id": False,
            }
        )
        self.plan.sequence_id = sequence
        self.analytic.code = "MANUAL"

        self.analytic.action_resequence()

        self.assertEqual(self.analytic.code, "NEXT/001")

    def test_resequence_falls_back_to_default_sequence(self):
        self.analytic.code = "MANUAL"

        self.analytic.action_resequence()

        self.assertTrue(self.analytic.code.startswith("AA"))
