from dataclasses import dataclass

import chess
from playwright.async_api import Page


@dataclass(frozen=True)
class BoardGeometry:
    selector: str = "[data-testid='board']"
    white_at_bottom: bool = True


async def click_uci_move(
    page: Page,
    move: chess.Move,
    geometry: BoardGeometry,
) -> None:
    source = await square_center(page, chess.square_name(move.from_square), geometry)
    target = await square_center(page, chess.square_name(move.to_square), geometry)

    await page.mouse.click(source[0], source[1])
    await page.mouse.click(target[0], target[1])


async def square_center(
    page: Page,
    square_name: str,
    geometry: BoardGeometry,
) -> tuple[float, float]:
    board = page.locator(geometry.selector)
    box = await board.bounding_box()
    if box is None:
        raise RuntimeError(f"Board selector did not resolve: {geometry.selector}")

    square_index = chess.parse_square(square_name)
    file_index = chess.square_file(square_index)
    rank_index = chess.square_rank(square_index)

    if geometry.white_at_bottom:
        column = file_index
        row = 7 - rank_index
    else:
        column = 7 - file_index
        row = rank_index

    square_size = box["width"] / 8
    x = box["x"] + (column + 0.5) * square_size
    y = box["y"] + (row + 0.5) * square_size
    return x, y
