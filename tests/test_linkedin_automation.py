import unittest
from unittest.mock import MagicMock, patch, mock_open
from selenium.common.exceptions import NoSuchElementException


class TestLinkedinBotRecommended(unittest.TestCase):

    @patch("selenium.webdriver.Chrome")
    def test_recommended_bot_init(self, mock_chrome):
        from LINKEDIN.recommended_page import LinkedinBot

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        bot = LinkedinBot()
        self.assertEqual(bot.page_number, 1)
        mock_driver.get.assert_called_with("https://www.linkedin.com/jobs/recommended/")

    @patch("selenium.webdriver.Chrome")
    def test_apply_job_clicks_easy_apply_and_actions(self, mock_chrome):
        from LINKEDIN.recommended_page import LinkedinBot

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        bot = LinkedinBot()

        # Mock easy apply button
        easy_apply_btn = MagicMock()
        easy_apply_btn.is_displayed.return_value = True
        easy_apply_btn.is_enabled.return_value = True

        # Mock action button
        action_btn = MagicMock()
        action_btn.is_displayed.return_value = True
        action_btn.is_enabled.return_value = True

        def find_elements_side_effect(by, value):
            if "jobs-apply-button" in value or "Easy Apply" in value:
                return [easy_apply_btn]
            elif "Submit application" in value or "Next" in value or "Review" in value:
                # Return button on first call, empty list on subsequent calls to break loop
                if not getattr(find_elements_side_effect, 'called', False):
                    find_elements_side_effect.called = True
                    return [action_btn]
                return []
            return []

        mock_driver.find_elements.side_effect = find_elements_side_effect

        bot.apply_job()
        easy_apply_btn.click.assert_called()
        action_btn.click.assert_called()


class TestLinkedinBotSearch(unittest.TestCase):

    @patch("selenium.webdriver.Chrome")
    def test_search_bot_init(self, mock_chrome):
        from LINKEDIN.search_jobs import LinkedinBot

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        bot = LinkedinBot()
        self.assertEqual(bot.page_number, 1)
        mock_driver.get.assert_called_with("https://www.linkedin.com/jobs")

    @patch("selenium.webdriver.Chrome")
    def test_do_search_inputs_query(self, mock_chrome):
        from LINKEDIN.search_jobs import LinkedinBot

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        search_box = MagicMock()
        mock_driver.find_elements.return_value = [search_box]

        bot = LinkedinBot()
        bot.do_search("python developer", "remote")

        search_box.click.assert_called()
        search_box.send_keys.assert_called_with("python developer\n")


if __name__ == "__main__":
    unittest.main()
