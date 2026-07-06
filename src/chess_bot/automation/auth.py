from collections.abc import Awaitable, Callable
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Page

LoginFlow = Callable[[Page], Awaitable[None]]


class AuthSessionManager:
    """Persist Playwright storage state across internal test runs."""

    def __init__(self, storage_state_path: Path) -> None:
        self.storage_state_path = storage_state_path

    async def context(
        self,
        browser: Browser,
        base_url: str,
        login_flow: LoginFlow,
    ) -> BrowserContext:
        if self.storage_state_path.exists():
            return await browser.new_context(
                base_url=base_url,
                storage_state=str(self.storage_state_path),
            )

        context = await browser.new_context(base_url=base_url)
        page = await context.new_page()
        await login_flow(page)
        self.storage_state_path.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(self.storage_state_path))
        await page.close()
        return context
