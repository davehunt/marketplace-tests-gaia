# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import random

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceAddReview(MarketplaceGaiaTestCase):

    def test_add_review(self):
        account = self.create_firefox_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        app_name = home_page.first_free_app['name']

        home_page.login(account.email, account.password)
        details_page = home_page.navigate_to_app(app_name)

        current_time = str(time.time()).split('.')[0]
        rating = random.randint(1, 5)
        body = 'This is a test %s' % current_time

        review_page = details_page.tap_write_review()
        details_page = review_page.write_a_review(rating, body)

        details_page.wait_for_review_posted_notification()

        # Check if review was added correctly
        self.assertEqual(details_page.first_review_rating, rating)
        self.assertEqual(details_page.first_review_body, body)
