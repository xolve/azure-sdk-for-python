# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import datetime
import unittest

import azure.mgmt.consumption
import azure.mgmt.consumption.models
from devtools_testutils import AzureMgmtRecordedTestCase, ResourceGroupPreparer, recorded_by_proxy


class TestMgmtConsumption(AzureMgmtRecordedTestCase):

    def setup_method(self, method):
        self.consumption_client = self.create_mgmt_client(
            azure.mgmt.consumption.ConsumptionManagementClient
        )

    @ResourceGroupPreparer()
    @recorded_by_proxy
    def test_budgets(self, resource_group):
        SUBSCRIPTION_ID = self.get_settings_value('SUBSCRIPTION_ID')
        SCOPE = '/subscriptions/{}/resourceGroups/{}'.format(SUBSCRIPTION_ID, resource_group.name)
        BUDGET_NAME = self.get_resource_name('budget')
        # create
        BODY = {
            "category": "Cost",
            "amount": '100',
            "timeGrain": "Monthly",
            "timePeriod": {
                "startDate": "2022-01-01T00:00:00Z",
                "endDate": "2022-10-31T00:00:00Z"
            }
        }
        self.consumption_client.budgets.create_or_update(SCOPE, BUDGET_NAME, BODY)

        # get
        self.consumption_client.budgets.get(SCOPE, BUDGET_NAME)

        # delete
        self.consumption_client.budgets.delete(SCOPE, BUDGET_NAME)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
