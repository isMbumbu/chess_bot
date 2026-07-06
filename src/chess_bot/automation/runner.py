from pathlib import Path

from playwright.async_api import Page, async_playwright

from chess_bot.automation.auth import AuthSessionManager, LoginFlow
from chess_bot.automation.board_state import BoardSelectors, board_from_dom
from chess_bot.automation.engine import StockfishEngine
from chess_bot.automation.executor import BoardGeometry, click_uci_move


def form_login_flow(email: str, password: str) -> LoginFlow:
    async def login(page: Page) -> None:
        await page.goto("/login")
        await page.get_by_label("Email").fill(email)
        await page.get_by_label("Password").fill(password)
        await page.get_by_role("button", name="Sign in").click()
        await page.wait_for_url("**/dashboard")

    return login


async def run_internal_board_test(
    base_url: str,
    board_path: str,
    stockfish_path: Path,
    email: str,
    password: str,
    storage_state_path: Path = Path(".auth/storage-state.json"),
) -> None:
    session = AuthSessionManager(storage_state_path)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await session.context(
            browser,
            base_url,
            form_login_flow(email, password),
        )
        page = await context.new_page()

        await page.goto(board_path)
        board = await board_from_dom(page, BoardSelectors())

        async with StockfishEngine(stockfish_path) as engine:
            move = await engine.best_move(board)

        await click_uci_move(page, move, BoardGeometry())
        await context.close()
        await browser.close()
